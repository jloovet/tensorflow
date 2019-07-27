
# coding: utf-8

# In[3]:


import tensorflow as tf
import tensorflow.keras as kr
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


tf.__version__


# In[5]:


data = kr.datasets.mnist.load_data()


# In[79]:


images = data[0][0]
numbers = data[0][1]

imagesTest = data[1][0]
numbersTest = data[1][1]


# In[80]:


#konvertera fr 0-255 -> -1 - 1 för att passa keras lib
images = np.array(images, dtype='float')
images /= 255 
images -= 0.5
images *= 2

imagesTest = np.array(imagesTest, dtype='float')
imagesTest /= 255 
imagesTest -= 0.5
imagesTest *= 2


# In[81]:


plt.imshow(images[0])


# In[82]:


print(numbers[0])


# In[83]:


#skapa 100 noder i första lagret
layer_1 = kr.layers.Dense(100, kr.activations.relu)
#skapa 10 noder i outputlagret (1 per siffra)
layer_2 = kr.layers.Dense(10, kr.activations.sigmoid)


# In[84]:


kr.initializers.Initializer()


# In[85]:


@tf.function
def getOutput(x) :
    x = tf.reshape(x, [-1, 28 * 28])
    x = layer_1(x)
    x = layer_2(x)
    return x
    
    


# In[86]:


getOutput([images[0]])


# In[87]:


cce = tf.keras.losses.SparseCategoricalCrossentropy()
@tf.function
def getLoss(x,y) :
    #x alltid input, y alltid output
    prediction = getOutput(x)
    loss = cce(y, prediction)
    return loss


# In[88]:


getLoss(images[0:1000], numbers[0:1000])


# In[89]:


opt = kr.optimizers.Adam(learning_rate=0.01)


# In[90]:


@tf.function
def train(x,y) :
    tranableVariables = layer_1.trainable_variables + layer_2.trainable_variables
    with tf.GradientTape() as t:
        t.watch(tranableVariables)
        loss = getLoss(x,y)
    grads = t.gradient(loss, tranableVariables) 
    opt.apply_gradients(zip(grads, tranableVariables))
        


# In[49]:


train(images[0:1000], numbers[0:1000])


# In[91]:


batchSize = 1024
def trainAll() :
    for i in range(0,len(images), batchSize) :
        batchImages = images[i:i+batchSize]
        batchNumbers = numbers[i:i+batchSize]
        train(batchImages, batchNumbers)


# In[99]:


for epoch in range(5) :
    print("Epoch", epoch)
    trainAll()
    print("Loss", getLoss(imagesTest[0:1000], numbersTest[0:1000]))


# In[95]:


predictions = getOutput(imagesTest[0:10])
for i in range(10) :
    plt.imshow(imagesTest[i])
    plt.show()
    print(np.argmax(predictions.numpy()[i]))
    

