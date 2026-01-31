using UnityEngine;
using System;
using System.Net;
using uPLibrary.Networking.M2Mqtt; 
using uPLibrary.Networking.M2Mqtt.Messages;
using TMPro;

public class Packet : MonoBehaviour
{
    // Start is called once before the first execution of Update after the MonoBehaviour is created

    // variable
    public float scale_packet = 1.0f;

    // display
    public TextMeshProUGUI displayText;
    public TextMeshProUGUI displayText_saved;
    public TextMeshProUGUI displayText_warning;
    public TextMeshProUGUI displayText_help;

    // settings for MQTT
    public string ipAddress = "127.0.0.1"; 
    public string mqttTopic = "warehouse/packet/data";
    private string username = "HA_warehouse";
    private string password = "qweasd";
    
    private MqttClient mqttClient;
    private string lastReceived = "";

    // data fields
    public float axe_x, axe_y, axe_z;
    public bool light1, light2;
    private float area, perimeter, volume;
    private float base_x=0, base_y=0, base_z=0;
    private bool isBaseSet = false;
    private float cal_x=0, cal_y=0, cal_z=0;
    private float saved_x=0, saved_y=0, saved_z=0, saved_area=0, saved_perimeter=0, saved_volume=0;
    private bool isSaved = false;
    private bool isWarningDisplayed = false;
    private bool isHelpDisplayed = true;

    void Start()
    {
        // init connection
        mqttClient = new MqttClient(IPAddress.Parse(ipAddress));
        mqttClient.MqttMsgPublishReceived += clientMqttMsgPublishReceived;

        string clientId = Guid.NewGuid().ToString();
        mqttClient.Connect(clientId, username, password); 

        // subscribe to topic
        mqttClient.Subscribe(new string[] { mqttTopic }, new byte[] { MqttMsgBase.QOS_LEVEL_AT_MOST_ONCE });
        Debug.Log("MQTT Connected and Subscribed to " + mqttTopic);

        // initial display update
        displayText.fontSize = 12;
        displayText.enableAutoSizing = true;
        displayText.alignment = TextAlignmentOptions.TopLeft;

        displayText_saved.fontSize = 12;
        displayText_saved.enableAutoSizing = true;
        displayText_saved.alignment = TextAlignmentOptions.TopRight;

        displayText_warning.fontSize = 24;
        displayText_warning.enableAutoSizing = true;
        displayText_warning.alignment = TextAlignmentOptions.Center;

        displayText_help.fontSize = 24;
        displayText_help.enableAutoSizing = true;
        displayText_help.alignment = TextAlignmentOptions.Center;

        if (isHelpDisplayed)
        {
            OpenMenu();
        }

        // init base values
        OnBaseButtonPressed();
    }

    void clientMqttMsgPublishReceived(object sender, MqttMsgPublishEventArgs e)
    {
        Debug.Log("a message just arrived");
        lastReceived = System.Text.Encoding.UTF8.GetString(e.Message);
        Debug.Log("Raw Data: " + lastReceived);
    }

    // Update is called once per frame
    void Update()
    {
        if (isHelpDisplayed)
        {
            OpenMenu();
            // avalaesh bayad mtn haye dige ro pak konam bad in ha jash neveshte beshe
            if (Input.GetKeyDown(KeyCode.Space) || Input.GetKeyDown(KeyCode.Escape))
            {
                CloseMenu();
            }
        }

        else // stop another process when help is displayed
        {
            // when received new data, parse it
            if (!string.IsNullOrEmpty(lastReceived))
            {
                try {
                    // split data by '-'
                    string[] data = lastReceived.Split('-');

                    if (data.Length == 5) {
                        axe_x =  float.Parse(data[0]);
                        axe_y =  float.Parse(data[1]);
                        axe_z =  float.Parse(data[2]);
                        if (data[3] == "1"){light1 = true;}
                        else {light1 = false;}
                        if (data[4] == "1") {light2 = true;}
                        else {light2 = false;}
                    }
                    
                    if (isBaseSet) {
                        cal_x = base_x - axe_x;
                        cal_y = base_y - axe_y;
                        cal_z = base_z - axe_z;
                        area = cal_x * cal_y;   
                        perimeter = 2 * (cal_x + cal_y);
                        volume = cal_x * cal_y * cal_z; 
                    }  
                    
                    if (light1 && light2){ 
                        Debug.Log("Both sensors are ON - Packet detected correctly.");
                        isWarningDisplayed = true;
                    }   

                    if (!light1 || !light2){
                        isWarningDisplayed = false;
                    }

                    // logic to apply the data
                    set_size();                        

                }
                catch (Exception ex) {
                    Debug.LogError("Parsing Error: " + ex.Message);
                }
            }

                if (Input.GetKeyDown(KeyCode.Space)) {OnSaveButtonPressed();}
                if (Input.GetKeyDown(KeyCode.L)) {OnDelButtonPressed();}
                if (Input.GetKeyDown(KeyCode.B)) {OnBaseButtonPressed();}
                if (Input.GetKeyDown(KeyCode.I)) {isHelpDisplayed = true;}

                // update display
                UpdateDisplay();
                UpdateDisplay_saved();
                UpdateDisplay_Warning(); 

                lastReceived = ""; // reset after processing
        }
    }

    public void CloseMenu()
    {
        displayText_help.text = $"";
        isHelpDisplayed = false;
    }

    public void OpenMenu()
    {
        displayText.text = $"";
        displayText_saved.text = $"";   
        displayText_warning.text = $"";
        isHelpDisplayed = true;
        displayText_help.text = $"<b>HELP MENU</b>\n" +
                                $"------------------\n" +
                                $"Verwenden Sie die Pfeiltasten, um die Kamera zu drehen.\n" +
                                $"Verwenden Sie Z/X zum Vergrößern/Verkleinern.\n\n" +
                                $"Drücken Sie 'I', um die Info zu öffnen.\n" +
                                $"<color=green>Drücken Sie 'B' oder 'Base Button', um die Basisabmessungen einzustellen (beide Sensoren AUS).</color>\n" +
                                $"<color=blue>Drücken Sie die Leertaste oder 'Speichern Button', um die aktuellen Messwerte zu speichern (beide Sensoren EIN).</color>\n" +
                                $"<color=red>Drücken Sie 'L' oder 'Löschen Button', um gespeicherte Messwerte zu löschen.</color>\n\n" +
                                $"<color=yellow>Drücken Sie die Taste Info oder die Taste 'Esc' oder 'Leertaste', um dieses Menü zu schließen.</color>";

    }

    public void OnInfoButtonPressed()
    {
        if (isHelpDisplayed)
        {
            CloseMenu();
            isHelpDisplayed = false;
        }
        else
        {
            OpenMenu();
            isHelpDisplayed = true;
        }
    }

    void UpdateDisplay()
    {   
        if (displayText != null)
        {
            displayText.text = $"LOGISTICS DASHBOARD\n" +
                           $"------------------\n" +
                           $"<color=red>X: {cal_x :F1} cm</color>\n" +
                           $"<color=green>Y: {cal_y:F1} cm</color>\n" +
                           $"<color=blue>Z: {cal_z:F1} cm</color>\n" +
                           $"Sensor 1: {(light1 ? "ON" : "OFF")}\n" +
                           $"Sensor 2: {(light2 ? "ON" : "OFF")}\n" +
                           $"PERI: {perimeter:F1} cm\n" +
                           $"AREA: {area:F1} cm²\n" +
                           $"VOL: {volume:F1} cm³\n\n" +
                           $"base: X={base_x} Y={base_y} Z={base_z}";
        }
    }

    void UpdateDisplay_saved()
    {   
        if (displayText_saved != null && isSaved)
        {
            displayText_saved.text = $"Saved\n" +
                           $"------------------\n" +
                           $"<color=red>X: {saved_x :F1} cm</color>\n" +
                           $"<color=green>Y: {saved_y:F1} cm</color>\n" +
                           $"<color=blue>Z: {saved_z:F1} cm</color>\n" +
                           $"PERI: {saved_perimeter:F1} cm\n" +
                           $"AREA: {saved_area:F1} cm²\n" +
                           $"VOL: {saved_volume:F1} cm³";
        }
    }

    void UpdateDisplay_Warning()
    {
        if (displayText_warning != null && isWarningDisplayed)
        {
            displayText_warning.text = $"<color=red><b>WARNING: HAND WEG!</b></color>\n" +
                                       $"<color=yellow>Drück BTN Rechnen</color>";
        }

        else if (displayText_warning != null)
        {
            displayText_warning.text = $"";
        }
    }

    void set_size()
    {
        transform.localScale = new Vector3(axe_x * scale_packet, axe_y * scale_packet, axe_z * scale_packet);
    }

    public void OnBaseButtonPressed()
    {
        Debug.Log("btn base pressed");
        if (!light1 && !light2 && (axe_x != 0 || axe_y != 0 || axe_z != 0))
        {
            base_x = axe_x;
            base_y = axe_y;
            base_z = axe_z;
            isBaseSet = true;
        }
    }

    public void OnSaveButtonPressed()
    {
        Debug.Log("btn save pressed");
        if (light1 && light2)
        {
        // Save the current calculated values
        saved_x = cal_x;
        saved_y = cal_y;
        saved_z = cal_z;
        saved_area = area;
        saved_perimeter = perimeter;
        saved_volume = volume;
        isSaved = true;
        isWarningDisplayed = false;
        }

        else
        {
            Debug.Log("Cannot save: Both sensors must be ON.");
            if (displayText_saved != null)
            {
                displayText_saved.text = $"<color=red><b>ERROR: Both sensors must be ON to save data.</b></color>";
            }
        }
    }

    public void OnDelButtonPressed()
    {
        Debug.Log("btn Del pressed");
        saved_x = 0;
        saved_y = 0;
        saved_z = 0;
        saved_area = 0;
        saved_perimeter = 0;
        saved_volume = 0;
        isSaved = false;
        isWarningDisplayed = false;
        if (displayText_saved != null) {displayText_saved.text = $"";}
    }

   
}