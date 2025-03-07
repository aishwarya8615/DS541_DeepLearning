# -*- coding: utf-8 -*-
"""homework5_kagrawal.ipynb

Automatically generated by Colaboratory.

"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize  # For check_grad, approx_fprime

class RNN:
    def __init__ (self, numHidden, numInput, numOutput):
        self.numHidden = numHidden
        self.numInput = numInput
        self.U = np.random.randn(numHidden, numHidden) * 1e-1
        self.V = np.random.randn(numHidden, numInput) * 1e-1
        self.w = np.random.randn(numHidden) * 1e-1
        self.w = np.reshape(self.w,(numHidden,1))
      
    def backward (self,x,y,h,yhat):
        dJ_dw=0
        dJ_dU=0
        dJ_dV=0
        dyhat_dh = np.reshape(self.w,(self.w.shape[0],1))
        dh_dU=0
        dh_dV=0
        for i in range(len(yhat)):
          dJ_dyhat = yhat[i]-y[i]
          dJ_dw += np.dot(h[i+1],dJ_dyhat)
          
          dh_dz = np.diag(np.diag(1-np.dot(h[i+1],h[i+1].T)))
          
          if i==0:
            dh_dU = np.dot(h[i].T,dh_dz)
            dh_dV = np.dot(dh_dz,x[i])
          else:
            dh_dU = np.dot(h[i].T,dh_dz) + np.dot(dh_dU,np.dot(self.U,dh_dz))
            dh_dV = np.dot(dh_dz,x[i]) + np.dot(dh_dV,np.dot(self.U,dh_dz))
          dh_dV1 = np.reshape(np.diag(dh_dV),(dh_dV.shape[0],1))
          dJ_dU += np.dot(np.dot(dyhat_dh,dJ_dyhat),dh_dU)
          dJ_dV += np.multiply(np.dot(dyhat_dh,dJ_dyhat),dh_dV1)
        return dJ_dw,dJ_dU,dJ_dV


    def forward (self, x):
      h=[]
      yhat=[]
      h.append(np.zeros((numHidden,1)))
      z = []
      for i in range(len(x)):
        z.append((np.dot(self.U,h[i])+np.dot(x[i],self.V)))
        h.append(np.tanh(z[i]))
        yhat.append(np.dot(h[i+1].T,self.w))
      return h, yhat
    
    def SGD(self,x,y):
        lr_U = 1e-5
        lr_V = 1e-7
        lr_w = 1e-1
        iteration=25000
        n_batch=1
        yhat=[]
        x = np.array(x)
        y = np.array(y)
        for _ in range(iteration): 
          h,yhat = self.forward(x)
          dJ_dw,dJ_dU,dJ_dV =self.backward(x,y,h,yhat)
          self.w = self.w - lr_w*dJ_dw
          self.U = self.U - lr_U*dJ_dU
          self.V = self.V - lr_V*dJ_dV
          J=self.compute_cost(y,yhat)
          print('cost:',J)
          
          
    def compute_cost(self,ys,yhat):
      J=0
      for i in range(len(ys)):
        J += (yhat[i]-ys[i])**2
      J=J/2
      return J

# From https://medium.com/@erikhallstrm/hello-world-rnn-83cd7105b767
def generateData ():
    total_series_length = 50
    echo_step = 2  # 2-back task
    batch_size = 1
    x = np.random.choice(2, total_series_length, p=[0.5, 0.5])
    y = np.roll(x, echo_step)
    y[0:echo_step] = 0
    y = list(y)
    return (x, y)

if __name__ == "__main__":
    xs, ys = generateData()
#     print(xs)
#     print(ys)
    numHidden = 6
    numInput = 1
    numTimesteps = len(xs)
    rnn = RNN(numHidden, numInput, 1)
    rnn.SGD(xs,ys)

