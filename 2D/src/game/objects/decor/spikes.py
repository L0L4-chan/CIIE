'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''


from game.objects.decor.platforms import Platforms
#Clase que define las plataformas con pinchos, esta nueva clase nos permite 
#diferenciarlas de las plataformas normales y poder tratarlas de forma distinta
#en las collisiones con el jugador.
class Spikes(Platforms):
    
    def __init__(self, x = 0, y = 0, width = 0, height = 18 ):
        """
        Constructor de la clase Spike.

        :param x: Posición inicial en X.
        :param y: Posición inicial en Y.
        :param width: Ancho de la plataforma.
        :param height: Alto de la plataforma.
        :return: None
        """
        super().__init__(x,y,width, height) 
     
       

        
 
    