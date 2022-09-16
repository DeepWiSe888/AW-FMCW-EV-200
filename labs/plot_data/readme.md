##### use python environment

1. First device connection to computer.

2. Install dependent libraries:
    ```python
    pip install -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple/
    ```
3. Changing the serial name in the main function.
    ```
    def main():
        recv = SerialCollect("COM3")
        collect = threading.Thread(target=recv.recv)
        collect.setDaemon(True)
        collect.start()
        #....
    ```
4. Run plot data program in terminal:
    ```s
    python plot_demo.py
    ```

##### use conda virtual environment
1. install anaconda and update conda
    ```
    #install anaconda

    #update conda
    conda update conda
    ```
2. creat python environment
    ```
    conda create -n py39 python=3.9
    ``` 
3. activate env
    ```
    #linux
    source activate py39

    #windows
    activate py39
    ```
4. install libs
    ```
    # requirements.txt,
    # the installation package version is automatically selected
    numpy
    scipy
    pyqtgraph
    pyserial
    PyOpenGL
    spyder
    PyQt5

    #install 
    pip install -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple/

    ```
5. run
    ```
    # change the serial port name and plot data
    python plot_demo.py
    ```
##### Tested Environment(s)
1. Python:3.7.9
    ```
    1. Python version:3.7.9
    2. PyQtGraph version:0.12.2
    3. PyQt5 version:5.15.4
    4. NumPy version:1.19.5
    5. Scipy version:1.5.2
    6. PyOpenGl version:3.1.5
    7. Spyder version:5.1.1
    8. PySerial version:3.5
    ```
2. Python:3.9.6
    ```
    1. Python version:3.9.6
    2. PyQtGraph version:0.12.2
    3. PyQt5 version:5.12.3
    4. NumPy version:1.21.2
    5. Scipy version:1.7.1
    6. PyOpenGl version:3.1.5
    7. Spyder version:5.1.1
    8. PySerial version:3.5
    ```