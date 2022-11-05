from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
from PIL import Image
from gpu_shape import GPUShape

#Setea unos assets específicos en un modo determinado a una figura de manera
#sencilla e intuitiva.
def textureSimpleSetup(imgName, sWrapMode, tWrapMode, minFilterMode, maxFilterMode):
     # wrapMode: GL_REPEAT, GL_CLAMP_TO_EDGE
     # filterMode: GL_LINEAR, GL_NEAREST
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    
    # texture wrapping params
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, sWrapMode)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, tWrapMode)

    # texture filtering params
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, minFilterMode)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, maxFilterMode)
    
    image = Image.open(imgName)
    img_data = np.array(image, np.uint8)

    if image.mode == "RGB":
        internalFormat = GL_RGB
        format = GL_RGB
    elif image.mode == "RGBA":
        internalFormat = GL_RGBA
        format = GL_RGBA
    else:
        print("Image mode not supported.")
        raise Exception()

    glTexImage2D(GL_TEXTURE_2D, 0, internalFormat, image.size[0], image.size[1], 0, format, GL_UNSIGNED_BYTE, img_data)

    return texture

#Shader capaz de utilizar varias luces, además del manejo de texturas, modelo, vista, proyección y el uso
#de matrices de transformación.
class MultipleLightTexturePhongShaderProgram:

    def __init__(self):
        vertex_shader = """
            #version 330 core

            in vec3 position;
            in vec2 texCoords;
            in vec3 normal;

            out vec3 fragPosition;
            out vec2 fragTexCoords;
            out vec3 fragNormal;

            uniform mat4 model;
            uniform mat4 view;
            uniform mat4 projection;

            void main(){
                fragPosition = vec3(model * vec4(position, 1.0));
                fragTexCoords = texCoords;
                fragNormal = mat3(transpose(inverse(model))) * normal;  
                gl_Position = projection * view * vec4(fragPosition, 1.0);
            }        
            """
        
        fragment_shader = """
            #version 330 core

            in vec3 fragNormal;
            in vec3 fragPosition;
            in vec2 fragTexCoords;

            out vec4 fragColor;

            struct PointLight {
                vec3 position;
                float constant;
                float linear;
                float quadratic;
                vec3 diffuse;
                vec3 specular;
            };

            struct SpotLight {
                vec3 position;
                vec3 direction;
                float cutOff;
                float outerCutOff;
                float constant;
                float linear;
                float quadratic;
                vec3 diffuse;
                vec3 specular;       
            };

            uniform int point_lights;
            uniform int spot_lights;
            //Se asume un máximo de 10 point y spot lights.
            uniform PointLight pointLights[10];
            uniform SpotLight spotLights[10];
            
            uniform vec3 viewPosition; 
            uniform vec3 ambientLight;
            uniform sampler2D samplerTex;
            uniform float shininess;

            vec3 CalcPointLight(PointLight light, vec3 normal, vec3 fragPos, vec3 viewDir);
            vec3 CalcSpotLight(SpotLight light, vec3 normal, vec3 fragPos, vec3 viewDir);

            void main(){
                vec3 norm = normalize(fragNormal);
                vec3 viewDir = normalize(viewPosition - fragPosition);
                vec3 result = vec3(0.0,0.0,0.0);

                for(int i = 0; i <point_lights; i++)
                    result += CalcPointLight(pointLights[i], norm, fragPosition, viewDir);

                for(int i = 0; i < spot_lights; i++)
                    result += CalcSpotLight(spotLights[i], norm, fragPosition, viewDir);

                result += ambientLight;

                vec4 fragOriginalColor = texture(samplerTex, fragTexCoords);
                vec3 resultFinal = result * fragOriginalColor.rgb;

                fragColor = vec4(resultFinal, 1.0);
            }

            //Calcula la intensidad usando un pointLight.
            vec3 CalcPointLight(PointLight light, vec3 normal, vec3 fragPos, vec3 viewDir){
                vec3 lightDir = normalize(light.position - fragPos); //L

                //Intensidad por reflexión difusa
                float diff = max(dot(normal, lightDir), 0.0);
                vec3 diffuse = light.diffuse * diff; 

                //Intensidad por reflexión especular
                vec3 reflectDir = reflect(-lightDir, normal);
                float spec = pow(max(dot(viewDir, reflectDir), 0.0), shininess);
                vec3 specular = light.specular * spec; 
              
                //Atenuación debido a la distancia
                float distance = length(light.position - fragPos);
                float attenuation = 1.0 / (light.constant + light.linear * distance + light.quadratic * (distance * distance));    
            
                diffuse *= attenuation;
                specular *= attenuation;
                return diffuse + specular;
            }

            //Calcula la intensidad usando un spotLight.
            vec3 CalcSpotLight(SpotLight light, vec3 normal, vec3 fragPos, vec3 viewDir){
                vec3 lightDir = normalize(light.position - fragPos);
                
                //Intensidad por reflexión difusa
                float diff = max(dot(normal, lightDir), 0.0);
                vec3 diffuse = light.diffuse * diff;

                //Intensidad por reflexión especular
                vec3 reflectDir = reflect(-lightDir, normal);
                float spec = pow(max(dot(viewDir, reflectDir), 0.0), shininess);
                vec3 specular = light.specular * spec;

                //Atenuación debido a la distancia
                float distance = length(light.position - fragPos);
                float attenuation = 1.0 / (light.constant + light.linear * distance + light.quadratic * (distance * distance));    

                //Intensidad del spotLight
                float theta = dot(lightDir, normalize(-light.direction)); 
                float epsilon = light.cutOff - light.outerCutOff;
                float intensity = clamp((theta - light.outerCutOff) / epsilon, 0.0, 1.0);

                diffuse *= attenuation * intensity;
                specular *= attenuation * intensity;

                return diffuse + specular;
            }
            """
        
        # Binding artificial vertex array object for validation
        VAO = glGenVertexArrays(1)
        glBindVertexArray(VAO)

        self.shaderProgram = OpenGL.GL.shaders.compileProgram(
            OpenGL.GL.shaders.compileShader(vertex_shader, OpenGL.GL.GL_VERTEX_SHADER),
            OpenGL.GL.shaders.compileShader(fragment_shader, OpenGL.GL.GL_FRAGMENT_SHADER))

    def setupVAO(self, gpuShape):

        glBindVertexArray(gpuShape.vao)

        glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)

        # 3d vertices + rgb color + 3d normals => 3*4 + 2*4 + 3*4 = 32 bytes
        position = glGetAttribLocation(self.shaderProgram, "position")
        glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
        glEnableVertexAttribArray(position)
        
        color = glGetAttribLocation(self.shaderProgram, "texCoords")
        glVertexAttribPointer(color, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
        glEnableVertexAttribArray(color)

        normal = glGetAttribLocation(self.shaderProgram, "normal")
        glVertexAttribPointer(normal, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(20))
        glEnableVertexAttribArray(normal)

        # Unbinding current vao
        glBindVertexArray(0)

    def drawCall(self, gpuShape, mode=GL_TRIANGLES):
        assert isinstance(gpuShape, GPUShape)
        # Binding the VAO and executing the draw call
        glBindVertexArray(gpuShape.vao)
        glBindTexture(GL_TEXTURE_2D, gpuShape.texture)
        glDrawElements(mode, gpuShape.size, GL_UNSIGNED_INT, None)
        # Unbind the current VAO
        glBindVertexArray(0)