# -*- coding: utf-8 -*-
'''Constants for the application.'''

# a_type
# MANUAL = 'manual'
# AUTOMATIC = 'automatic'

# File filtering informations
OLD_INPUT_FILE_EXTENSION = '.nta' # Servo I - old input file format extension
NEW_INPUT_FILE_EXTENSION = '.sta' # Servo U - old input file format extension
RR_REGEX = 'TrendRRInspTime'
SERVO_REGEX = 'ServoCurveData'
VOLUME_REGEX = 'TrendTidalVolume'
BREATH_REGEX = 'Breath_'
CURVES_REGEX = 'Curves_'


# Dimension
FRAME_SELECT_WIDTH = 350
FRAME_SELECT_HEIGHT = 100

FRAME_CLASSIFICATION_WIDTH = 350
FRAME_CLASSIFICATION_HEIGHT = 350

FRAME_RESULT_WIDTH = 350
FRAME_RESULT_HEIGHT = 250

# Number of points rendered on the X axes.
PLOT_RANGE = 300

# Button Colors
LIGHT_GREEN = '#8BC34A'
ACTIVE_LIGHT_GREEN = '#9CCC65'
LIGHT_BLUE = '#3F51B5'
ACTIVE_LIGHT_BLUE = '#5C6BC0'
LIGHT_RED = '#F44336'
ACTIVE_LIGHT_RED = '#EF5350'
LIGHT_VIOLET = '#9C27B0'
ACTIVE_LIGHT_VIOLET = '#AB47BC'

BACKGROUND_COLOR = '#ECEFF1'

# Font
BUTTON_FONT = ('courier', 12)
BUTTON_BIG_FONT = ('courier', 15, 'bold')
BUTTON_BOLD_FONT = ('courier', 12, 'bold')
LABEL_TITLE_FONT = ('sans serif', 12, 'bold')
LABEL_DESCRIPTION_FONT = ('sans serif', 10)

# INITIAL FRAME LABELS
TITLE_MENU = 'P/I Classifier'
MANUAL_BUTTON_TEXT = 'Classificazione\nManuale'
AUTOMATIC_BUTTON_TEXT = 'Classificazione\nAutomatica'

TITLE_INSERT = 'Inserire i file di input'
TITLE_CLASSIFICATION = 'Classificazione'

# Insert Phase
# initial value of selection phase.
DEFAULT_ALPHA_TRESHOLD = 0.05
INSERT_WORKING_DIRECTORY = "Selezionare Working Directory\n (file da classificare):"
INSERT_LEARN_DIRECTORY = "Selezionare Directory della\n Knowledge Base:"
SENSIBILITY_LABEL = "Sensibilità: "
ASKSENSIB_TITLE = "Inserisci"
ASKSENSIB_MESSAGE = "Inserisci il livello di sensibilità.\nDefault " + str(DEFAULT_ALPHA_TRESHOLD) + ". Accettato (0-1)."

# Classification Phase
CLASSIFICATION_PLOT_TITLE = 'Grafico'
CLASSIFICATION_VALUES_TITLE = 'Valori'
MATRICIONE_CSV_NAME = "Matricione.csv"
CURVE_EADI_CSV_NAME = "Curve_Eadi.csv"
POPUP_C_TITLE = "Lavoro già presente"
POPUP_C_MESSAGE = "È presente del lavoro già fatto\nsu questo paziente.\n\nAprirlo e continuare?"
POPUP_C_MESSAGE_AUTOM = "È presente del lavoro  già fatto su questo paziente.\n" \
                        "La classificazione automatica sovrascriverà il vecchio lavoro.\n\n" \
                        "Procedere comunque?"
SERVO_INPUT_FILE = 'Servo Curve Data'
TIDAL_INPUT_FILE = 'Trend Tidal Volume'
RR_INPUT_FILE = 'Trend RR Insp'
OK_COLOR_CURVE = 'b'
ANOMALY_COLOR_CURVE = 'r'
DUBIOUS_COLOR_CURVE = 'm'

# RESULT FRAME
ASK_DATASET_TITLE = "Dataset Creato"
ASK_DATASET_DESCR = "Il dataset è stato creato correttamente.\n" \
                    "Vuoi includerlo all'interno dei file di learning,\n" \
                    "in modo da migliorare le prossime previsioni?"
WARNING_VERIFY_TITLE = "Seleziona"
WARNING_VERIFY_DESCR = "Seleziona almeno un elemento\ndalle checkbox."
VERIFY_BUTTON_TEXT = "Verifica"
MENU_BUTTON_TEXT = "Menu"
DATASET_BUTTON_TEXT = "Crea Dataset"
WARNING_ERROR = "Errore"
WARNING_DOUBIOUS_PRESENT = "Impossibile creare il dataset.\nCi sono ancora delle curve dubbie da classificare."

# Curve's classification Constants
ANOMALY = 0
OK = 1
DUBIOUS = 2

# Dataset Processor
# max number of concavity before and after.
NUM_MAX_CONCAVITY = 50
# max number of concavity in csv
NUM_MAX_CONCAVITY_CSV = 3

# learning_files path
DATASET_NAME = "dataset.csv"
LEARNING_FILES_PATH = "./RScript/learning_files/"
R_SCRIPT = 'Rscript'
R_SCRIPT_PATH = './RScript/RScript.R'
