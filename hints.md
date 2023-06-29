# <span style="color:orange"> Support on behaviour using tika</span>
Note: these hints are coming when using ubuntu. Not sure about mac or windows

## <span style="color:blue">Parallelization.</span>
In case of too much parrallelisation, tike server will get retrying message. Reduce parrallel parameter in global_variables.py.<br>
Monitor the usage of your CPU, if you reach always 100% , reduce the parallelization.<br>
The disk migth be also the slowdown point. check the i/os<br>  


## <span style="color:blue">Tesseract</span>
Tika is using tesseract process. when cancelling the python script (ctrl-C or control-D), some tesseract processes are still running until the end of treatement, and it can takes few seconds.<br>
If you relaunch immediatly the python script, you migth get a wrong list of remaining files. It is due that the update is still running util th end of all completion, despite the stop of th escript.
Be patient, and wait a litle bit.

## <span style="color:blue">Java (only Linux)</span>
Java is using a lot of memory, and more you treat documents, more the jvm will use memory.<br>
Usually there is a garbage collector to clean java memory. But at the end of the script, I have added a java killer.<br>
Be carefull, it is not linked to the java of th eprgrtam yet. you could kill another java stack, so if some problems occurs on other java program, remove the call of the java kill.