using UnityEngine;

public class Cam : MonoBehaviour
{
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    public GameObject player;
    public int cam_euler_x = 40;
    public int cam_euler_y = -45;
    public int cam_euler_z = 0;
    public float cam_height = 4;    
    public float cam_vertical_distance = -6;
    public float cam_horizontal_distance = 6;

    public int cam_speed = 2;
    public float cam_zoom_speed = 0.5f;
    void Start()
    {
        cam_euler_x = 30;
        cam_euler_y = -45;
        cam_euler_z = 0;
        cam_height = 4;    
        cam_vertical_distance = -6;
        cam_horizontal_distance = 6;
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetKeyDown(KeyCode.UpArrow))
        {
            cam_horizontal_distance -= cam_zoom_speed;
            cam_vertical_distance = -1 * cam_horizontal_distance;
        }

        else if (Input.GetKeyDown(KeyCode.DownArrow))
        {
            cam_horizontal_distance += cam_zoom_speed;
            cam_vertical_distance = -1 * cam_horizontal_distance;
        }

        else if (Input.GetKeyDown(KeyCode.LeftArrow))
        {
            cam_euler_y -= cam_speed;
        }

        else if (Input.GetKeyDown(KeyCode.RightArrow))
        {
            cam_euler_y += cam_speed;
        }

        transform.position=player.transform.position  + new Vector3(cam_horizontal_distance, cam_height, cam_vertical_distance);
        transform.rotation=Quaternion.Euler(cam_euler_x, cam_euler_y, cam_euler_z);
        
    }
}