import os 
import numpy as np
from tensorflow.keras.models import Model ,load_model
from tensorflow.keras.preprocessing.image import load_img ,img_to_array
import matplotlib.pyplot as plt 



class FeatureMapsList(BaseException):
    pass

class Layers_preprocessing():
    

    def __init__(self ,model , layers_output_indices= None):
        self.model_setter(model)
        self.layers_setter(layers_output_indices)
    
        
        
    def model_setter(self , model):
        self.model = model
            
    def layers_setter(self ,layers_output_indices):
        if layers_output_indices == None:
            layers_output_indices = []
        self.layers_indices = list(set(layers_output_indices))
        self.outputs = []
        if len(self.layers_indices) >0 :
            self.outputs = [self.model.layers[layer_index].output for layer_index in self.layers_indices]
    
                
    @property    
    def __output_layers(self ):
       return [self.model.layers[layer_index] for layer_index in self.layers_indices]
    
    @__output_layers.setter
    def add_output_layers(self ,layers_seq):
        self.layers_indices = list(set(self.layers_indices + layers_seq))
        self.outputs.append([self.model.layers[layer_index].output for layer_index in self.layers_indices])
        
    @__output_layers.setter
    def remove_output_layers(self ,layers_seq):
        self.layers_indices=  list(filter(lambda x: x not in layers_seq ,self.layers_indices ) )
        self.outputs=[self.model.layers[layer_index].output for layer_index in self.layers_indices]

  
    
    
        
            
class Visualiser(Layers_preprocessing):
    
    def _visualise_preprocessing(self ,image_path , layer_index):
        self._create_model(image_path)
        if layer_index > len(self.outputs):
            raise FeatureMapsList("layer index out of feature maps range")
        self.__feature_map =  np.array(self.prediction[layer_index])
        self.__feature_map= self.__feature_map.reshape(self.__feature_map.shape[1] ,self.__feature_map.shape[2] ,
                                  self.__feature_map.shape[3])
    
    def _create_model(self , image_path):
        image = img_to_array(load_img(image_path , color_mode= 'grayscale', target_size =(64  ,64) ))
        self.__Model = Model( inputs =  self.model.inputs ,outputs =  self.outputs)
        self.prediction =  self.__Model.predict(image.reshape(1 ,64  ,64 ,1))
    
    
    def plot(self ,image_path  ,layer_index):
        subplot_images_position = {64 : (8 , 8) ,
                                   32 : (4 , 8) ,
                                   16 : (4 , 4)}
        self._visualise_preprocessing(image_path ,layer_index)
        for conv_layer_index in range(1 , self.__feature_map.shape[2]+1):
            plt.subplot(subplot_images_position[self.__feature_map.shape[2]][0] ,
                        subplot_images_position[self.__feature_map.shape[2]][1] ,
                        conv_layer_index) 
            plt.imshow(self.__feature_map[: ,: ,conv_layer_index-1]  ,cmap = "binary")
        
        plt.plot()
        
    def f_map(self ,index):
        return self.__feature_map.shape
    
