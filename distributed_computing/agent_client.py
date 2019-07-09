'''In this file you need to implement remote procedure call (RPC) client

* The agent_server.py has to be implemented first (at least one function is implemented and exported)
* Please implement functions in ClientAgent first, which should request remote call directly
* The PostHandler can be implement in the last step, it provides non-blocking functions, e.g. agent.post.execute_keyframes
 * Hints: [threading](https://docs.python.org/2/library/threading.html) may be needed for monitoring if the task is done
'''

import weakref
import xmlrpclib as rpc
import sys
import os
import threading
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'joint_control'))
from keyframes import hello

class PostHandler(object):
    '''the post hander wraps function to be excuted in paralle
    '''
    def __init__(self, obj):
        self.proxy = weakref.proxy(obj)

    def set_angle(self, joint_name, angle):
        '''non-blocking call of ClientAgent.set_angle'''
        # YOUR CODE HERE        
        thread = threading.Thread(target=self.proxy.set_angle, args=(joint_name, angle))
        thread.start()

    def execute_keyframes(self, keyframes):
        '''non-blocking call of ClientAgent.execute_keyframes'''
        # YOUR CODE HERE
        thread = threading.Thread(target=self.proxy.execute_keyframes, args=[keyframes])
        thread.start()

    def set_transform(self, effector_name, transform):
        '''non-blocking call of ClientAgent.set_transform'''
        # YOUR CODE HERE
        thread = threading.Thread(target=self.proxy.set_transform, args=[effector_name, transform])
        thread.start()


class ClientAgent(object):
    '''ClientAgent request RPC service from remote server
    '''
    # YOUR CODE HERE
    def __init__(self, rpcProxy):
        self.rpcProxy = rpcProxy
        self.post = PostHandler(self)

    def get_angle(self, joint_name):
        '''get sensor value of given joint'''
        # YOUR CODE HERE
        return self.rpcProxy.get_angle(joint_name)

    
    def set_angle(self, joint_name, angle):
        '''set target angle of joint for PID controller
        '''
        # YOUR CODE HERE
        self.rpcProxy.set_angle(joint_name, angle)
        return 0

    def get_posture(self):
        '''return current posture of robot'''
        # YOUR CODE HERE
        return self.rpcProxy.get_posture()

    def execute_keyframes(self, keyframes):
        '''excute keyframes, note this function is blocking call,
        e.g. return until keyframes are executed
        '''
        # YOUR CODE HERE
        self.rpcProxy.execute_keyframes(keyframes)
        return 0

    def get_transform(self, name):
        '''get transform with given name
        '''
        # YOUR CODE HERE
        return self.rpcProxy.get_transform(name)

    def set_transform(self, effector_name, transform):
        '''solve the inverse kinematics and control joints use the results
        '''
        # YOUR CODE HERE
        self.post.set_transform(effector_name, transform)
        return 0

if __name__ == '__main__':
    rpcProxy = rpc.ServerProxy("http://localhost:8000")
    agent = ClientAgent(rpcProxy)
    # TEST CODE HERE
    #print(agent.get_angle('LHipYawPitch'))
    agent.post.set_angle("LShoulderPitch",15)
    #agent.post.execute_keyframes(hello())


