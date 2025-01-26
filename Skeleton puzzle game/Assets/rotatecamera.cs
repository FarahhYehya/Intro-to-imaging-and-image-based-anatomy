using UnityEngine;

public class CameraRotateAroundObject : MonoBehaviour
{
    public Transform target; // The object around which the camera will rotate
    public float rotationSpeed = 5f; // Speed of the camera rotation
    public float distance = 10f; // Distance from the target object

    private float currentAngle = 0f; // The current horizontal rotation angle (Y-axis)
    private float verticalAngle = 0f; // The vertical angle (up/down tilt)
    private Vector3 offset; // The camera's offset from the target object

    void Start()
    {
        if (target != null)
        {
            offset = new Vector3(0, 0, -distance); // Set the initial offset
        }
    }

    void Update()
    {
        if (target != null)
        {
            HandleMouseInput();
            UpdateCameraPosition();
        }
    }

    // Handle mouse input to rotate the camera around the target
    void HandleMouseInput()
    {
        // Rotate horizontally with the mouse (left/right)
        if (Input.GetMouseButton(1)) // Right mouse button held down
        {
            currentAngle += Input.GetAxis("Mouse X") * rotationSpeed; // Mouse X-axis movement for horizontal rotation
            verticalAngle -= Input.GetAxis("Mouse Y") * rotationSpeed; // Mouse Y-axis movement for vertical rotation
            verticalAngle = Mathf.Clamp(verticalAngle, -80f, 80f); // Limit vertical angle to avoid flipping
        }
    }

    // Update the camera position based on the new rotation
    void UpdateCameraPosition()
    {
        if (target != null)
        {
            // Calculate the new rotation
            Quaternion rotation = Quaternion.Euler(verticalAngle, currentAngle, 0);

            // Update the camera's position
            transform.position = target.position + rotation * offset;

            // Make the camera always look at the target object
            transform.LookAt(target);
        }
    }
}