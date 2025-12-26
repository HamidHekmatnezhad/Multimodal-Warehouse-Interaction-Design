import json
import os

def load_data_from_json():
    """
    Lädt Daten aus einer JSON-Datei und gibt sie als Dictionary zurück.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "..", "data.json")

    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
        
    except FileNotFoundError:
        raise Exception("File not found. in load_data_from_json()")
        
    except json.JSONDecodeError:
        raise Exception("JSON decode error in load_data_from_json()")
    
    except Exception as e:
        raise Exception(f"ERROR: {e}")
    




    
def test():
    DATA = load_data_from_json()
    print(DATA)
    print(type(DATA))

    TOPIC_EXIST = DATA["topic"]["exist"]["path"]
    EXIT_QOS = DATA["topic"]["exist"]["qos"]

    print(TOPIC_EXIST, EXIT_QOS) 

if __name__ == "__main__":
    test()