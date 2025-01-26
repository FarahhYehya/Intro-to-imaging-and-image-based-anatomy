using UnityEngine;

public class PuzzlePieceRandomizer : MonoBehaviour
{
    [Header("Scatter Settings")]
    public Vector3 scatterCenter = Vector3.zero;  // The center of the scatter area
    public Vector3 scatterSize = new Vector3(3f, 3f, 3f);  // Size of the scatter box (width, height, depth)
    public float scatterForce = 5f;  // Force applied to parts
    public Vector3 rotationRange = new Vector3(360f, 360f, 360f);  // Range for random rotation on each axis

    [Header("Camera Settings")]
    public Camera mainCamera;  // Reference to the camera
    public float cameraDistanceFactor = 2f;  // How far the camera should be from the bounds

    [Header("Select Pieces")]
    public Transform[] selectedPieces;  // Array to hold selected puzzle pieces to randomize

    void Start()
    {
        ScatterSelectedParts();
        AdjustCameraToFit();
    }

    void ScatterSelectedParts()
    {
        // Check if there are selected pieces
        if (selectedPieces.Length == 0)
        {
            Debug.LogWarning("No pieces selected to randomize!");
            return;
        }

        // Loop through each selected part
        foreach (Transform part in selectedPieces)
        {
            // Randomize position within the scatter area
            float randomX = Random.Range(scatterCenter.x - scatterSize.x / 2, scatterCenter.x + scatterSize.x / 2);
            float randomY = Random.Range(scatterCenter.y - scatterSize.y / 2, scatterCenter.y + scatterSize.y / 2);
            float randomZ = Random.Range(scatterCenter.z - scatterSize.z / 2, scatterCenter.z + scatterSize.z / 2);
            Vector3 randomPosition = new Vector3(randomX, randomY, randomZ);

            part.position = randomPosition;

            // Apply random rotation to each part
            float randomRotationX = Random.Range(0f, rotationRange.x);
            float randomRotationY = Random.Range(0f, rotationRange.y);
            float randomRotationZ = Random.Range(0f, rotationRange.z);
            Vector3 randomRotation = new Vector3(randomRotationX, randomRotationY, randomRotationZ);
            part.rotation = Quaternion.Euler(randomRotation);

            // Optionally add a slight random force to make the parts feel dynamic
            Rigidbody rb = part.GetComponent<Rigidbody>();
            if (rb != null)
            {
                Vector3 randomForce = Random.insideUnitSphere * scatterForce;
                rb.AddForce(randomForce, ForceMode.Impulse);
            }
        }
    }

    void AdjustCameraToFit()
    {
        // Calculate the bounds of the selected parts
        Bounds bounds = new Bounds(transform.position, Vector3.zero);

        // Iterate over each selected part and adjust the bounds to include their renderer bounds
        foreach (Transform part in selectedPieces)
        {
            Renderer partRenderer = part.GetComponent<Renderer>();
            if (partRenderer != null)
            {
                bounds.Encapsulate(partRenderer.bounds);  // Include the bounds of each part's renderer
            }
        }

        // Determine the center of the bounds
        Vector3 boundsCenter = bounds.center;

        // Adjust the camera position based on the bounds
        Vector3 cameraDirection = (mainCamera.transform.position - boundsCenter).normalized;
        float distance = bounds.size.magnitude * cameraDistanceFactor;

        mainCamera.transform.position = boundsCenter - cameraDirection * distance;

        // Make sure the camera is looking at the center of the scattered parts
        mainCamera.transform.LookAt(boundsCenter);
    }
}