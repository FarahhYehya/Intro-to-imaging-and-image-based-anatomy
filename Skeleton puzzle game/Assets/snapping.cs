using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class Snapping : MonoBehaviour
{
    public Transform expectedReferencePiece;
    public float snapDistance = 0.8f;
    public bool isSnapped = false;
    public static int snappedPieceCount = 0;
    public static int totalPieces = 8;

    public TextMeshProUGUI completionText;
    public AudioSource snapAudioSource; // Audio source to play snapping sound

    void Update()
    {
        if (expectedReferencePiece != null && !isSnapped)
        {
            float distance = Vector3.Distance(transform.position, expectedReferencePiece.position);

            if (distance <= snapDistance)
            {
                SnapToPosition();
            }
        }
    }

    void SnapToPosition()
    {
        float snapProgress = 1f - Mathf.Exp(-Time.deltaTime * 10f / snapDistance);
        transform.position = Vector3.Lerp(transform.position, expectedReferencePiece.position, snapProgress);
        transform.rotation = Quaternion.Lerp(transform.rotation, expectedReferencePiece.rotation, snapProgress);

        transform.position = new Vector3(
            Mathf.Round(transform.position.x * 100f) / 100f,
            Mathf.Round(transform.position.y * 100f) / 100f,
            Mathf.Round(transform.position.z * 100f) / 100f
        );

        transform.rotation = Quaternion.Euler(
            Mathf.Round(transform.rotation.eulerAngles.x * 100f) / 100f,
            Mathf.Round(transform.rotation.eulerAngles.y * 100f) / 100f,
            Mathf.Round(transform.rotation.eulerAngles.z * 100f) / 100f
        );

        if (Vector3.Distance(transform.position, expectedReferencePiece.position) <= 0.01f &&
            Quaternion.Angle(transform.rotation, expectedReferencePiece.rotation) <= 0.1f)
        {
            transform.position = expectedReferencePiece.position;
            transform.rotation = expectedReferencePiece.rotation;
            Debug.Log("Piece is snapped to the correct reference point");

            isSnapped = true;
            snappedPieceCount++;

            if (snapAudioSource != null) // Play snap sound if AudioSource is assigned
            {
                snapAudioSource.Play();
            }

            CheckCompletion();
        }
    }

    void CheckCompletion()
    {
        if (snappedPieceCount == totalPieces)
        {
            ShowCompletionMessage();
        }
    }

    void ShowCompletionMessage()
    {
        if (completionText != null)
        {
            completionText.text = "All pieces are snapped! Puzzle Complete!";
        }
    }

    public void SetExpectedReferencePiece(Transform newReference)
    {
        expectedReferencePiece = newReference;
        isSnapped = false;
    }
}