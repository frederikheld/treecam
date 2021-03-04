"""
Module to test Python features
"""

class HelloWorld:

    def hello(self, name = None):
        message = 'Hello'
        
        if name:
            message += ' ' 
            message += name

        message += '!'

        print(message)
