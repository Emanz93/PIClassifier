# PIClassifier
PIClassifier: automatic classifier for the Muttini et al (2014) research. Classify the input breath curves in three classes and allow to understand if the P/I ratio is high enough.

The problem to solve was a ternary classi cation -- Yes, No, Maybe -- of signals generated by the activity of the diaphragm during a registration of five minutes. This work is a part of a bigger research [1] lead by Dr. Giorgio Villani.

A [report](https://github.com/Emanz93/PIClassifier/blob/master/Technical_Report.pdf)  has been wrote to explain the inner algorithm and implementation choices.

## Requirements
* Python 3
    * Python Tkinter Library
    * Python Numpy Library
    * Python Matplotlib Library
* R
    * RPart Library

## Usage
Open a terminal in the main folder and run:

    python3.X PIClassifier.py

Where X is the Python3 version installed on your system.


## References
[1] Muttini Stefano, Villani Pier Giorgio, Trimarco Roberta, Bellani Giacomo, Grasselli Giacomo, Patroniti Nicol.
    "Relation between peak and integral of the diaphragm electromyographic activity at different levels of support during weaning from mechanical ventilation: a physiologic study."
    Journal of Critical Care (2014), doi:10.1016/j.jcrc.2014.08.013

[2] Jiawei Han, Micheline Kamber, Jain Pei. "Data Mining - Concept and techniques." Third Edition. Elsevier 2012.
