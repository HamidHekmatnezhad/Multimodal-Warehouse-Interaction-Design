using UnityEngine;

public class Cam : MonoBehaviour
{
    public GameObject player;
    
    public float distance = 10.0f; 
    public float minDistance = 2.0f;
    public float maxDistance = 40.0f;
    public int maxEulerX = 90;
    public int minEulerX = 0;

    public float cam_zoom_speed = 0.01f;

    public float cam_euler_x = 30f; 
    public float cam_euler_y = -45f; 
    public float cam_speed = 0.01f;   

    void Start()
    {
        // initial settings
        distance = 30.0f; 
        minDistance = 2.0f;
        maxDistance = 40.0f;
        maxEulerX = 90;
        minEulerX = 0;
        cam_euler_x = 30f; 
        cam_euler_y = -45f; 

        cam_zoom_speed = 0.1f;
        cam_speed = 0.5f;   
    }

    void Update()
    {
        if (player == null) return;

        if (Input.GetKey(KeyCode.DownArrow)) {cam_euler_x -= cam_speed;}
        else if (Input.GetKey(KeyCode.UpArrow)) {cam_euler_x += cam_speed;}

        if (Input.GetKey(KeyCode.LeftArrow)) {cam_euler_y -= cam_speed;}
        else if (Input.GetKey(KeyCode.RightArrow)) {cam_euler_y += cam_speed;}

        if (Input.GetKey(KeyCode.Z)) {distance -= cam_zoom_speed;}
        else if (Input.GetKey(KeyCode.X)) {distance += cam_zoom_speed;}

        cam_euler_x = Mathf.Clamp(cam_euler_x, minEulerX, maxEulerX); 
        distance = Mathf.Clamp(distance, minDistance, maxDistance);

        Quaternion rotation = Quaternion.Euler(cam_euler_x, cam_euler_y, 0);
        Vector3 negDistance = new Vector3(0.0f, 0.0f, -distance);
        Vector3 position = rotation * negDistance + player.transform.position;

        transform.rotation = rotation;
        transform.position = position;
    }
}