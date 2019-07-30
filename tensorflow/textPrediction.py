
# coding: utf-8

# In[1]:


import tensorflow as tf
import tensorflow.keras as kr
import numpy as np
import random

SIZE = 30


# In[2]:


content = open("shakespeare.txt").read()


# In[3]:


len(content)


# In[4]:


#gissa tecken nummer 11
chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUWVXYZ., ?!\"\n':;-()_"
#gör one hot lista
def oneHot(ch) :
    if ch not in chars :
        i = -1
    else :    
        i = chars.index(ch)
    result = [0.0] * len(chars)
    result[i] = 1.0
    return result


    


# In[5]:


#gör lista av listor...
def oneHotString(chars) :
    return list(map(oneHot, chars))



# In[6]:


#skapa layers
#layer_1_inner = kr.layers.Dense(25, kr.activations.relu)
layer_1_inner = kr.layers.Dense(50, kr.activations.selu)

layer_1 = kr.layers.TimeDistributed(layer_1_inner, input_shape=(SIZE,len(chars)))

layer_2 = kr.layers.Dense(256, kr.activations.relu)
layer_3 = kr.layers.Dense(len(chars), kr.activations.sigmoid)


# In[7]:


kr.initializers.Initializer()


# In[8]:


#input är one hot på hela 20 tkn
#@tf.function
def getOutput(x) :
    x = layer_1(x)
    x = tf.reshape(x,(-1, SIZE*50))
    x = layer_2(x)
    x = layer_3(x)
    return x

    
    


# In[10]:


getOutput(np.array([oneHotString("x" * SIZE)]))


# In[11]:


cce = tf.keras.losses.CategoricalCrossentropy()
#@tf.function
def getLoss(x,y) :
    #x alltid input, y alltid output
    prediction = getOutput(x)
    loss = cce(y, prediction+0.0001)
    return loss


# In[12]:


opt = kr.optimizers.Adam(learning_rate=0.001)
@tf.function
def train(x,y) :
    tranableVariables = layer_1.trainable_variables + layer_2.trainable_variables + layer_3.trainable_variables
    with tf.GradientTape() as t:
        t.watch(tranableVariables)
        loss = getLoss(x,y)
    grads = t.gradient(loss, tranableVariables) 
    opt.apply_gradients(zip(grads, tranableVariables))
    return loss
        


# In[13]:


#skapa batchar


# In[14]:


batchSize = 256
def generateBatches() :
    for i in range(0,len(content)-SIZE, batchSize) :
        x = []
        y = []
        for sampleIndex in range(i, i+batchSize) :
            try :
                xAdd = oneHotString(content[sampleIndex:sampleIndex+SIZE])
                yAdd = oneHot(content[sampleIndex+SIZE])
                x.append(xAdd)
                y.append(yAdd)
            except IndexError as _ :
                break
        #gör iterator
        yield(np.array(x,dtype="float32"),np.array(y,dtype="float32"))
       
        
        


# In[15]:


def generateString(l) :
    startIndex = random.randrange(0, len(content) -SIZE)
    text = content[startIndex:startIndex+SIZE]
    for i in range(l) :
        probs = getOutput(np.array([oneHotString(text[-SIZE:])])).numpy()
        #best_idx = np.argmax(probs[0])
        #text += chars[best_idx]
        text += np.random.choice(list(chars), p=probs[0] / sum(probs[0]))
    return text
    


# In[ ]:


epoch = 0
while True :
    lossList = []
    iterator = generateBatches()

    cnt = 0
    for (x,y) in iterator :
        lossList.append(train(x,y).numpy())
        cnt += 1
        if cnt % 1000 == 0 :
            print("generateString:", generateString(100))
            print("count",cnt, "  Loss = ", getLoss(x,y))
            
            
        
    #skriv 10 exempel till fil för varje epoch (genomgång av testdatat)
    epoch += 1
    print("epoch", epoch)
    with open("save-" + str(epoch) + ".txt", "w") as f :
        f.write("Current loss: " + str(sum(lossList)/len(lossList)))  
        for i in range(10) :
            f.write("\n===== Ex " + str(i) + "==== \n")
            f.write(generateString(300)) 

