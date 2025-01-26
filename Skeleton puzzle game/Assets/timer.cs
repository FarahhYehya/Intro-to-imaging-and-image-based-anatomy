using UnityEngine;
using TMPro;
using UnityEngine.SceneManagement;

public class GameTimer : MonoBehaviour
{
    [Header("Timer Settings")]
    [Tooltip("Total time allowed for the game in seconds")]
    [SerializeField] private float totalGameTime = 60f;

    [Header("UI References")]
    [Tooltip("Text component to display the remaining time")]
    [SerializeField] private TextMeshProUGUI timerText;

    [Tooltip("Panel to show when time runs out")]
    [SerializeField] private GameObject failurePanel;

    [Tooltip("Panel to show when the player wins")]
    [SerializeField] private GameObject successPanel;

    [Header("Skeleton System")]
    [Tooltip("Skeleton system object to change color when the player wins")]
    [SerializeField] private Renderer skeletonRenderer;

    [Tooltip("Color to change the skeleton system to upon winning")]
    [SerializeField] private Color winColor = Color.red;

    // Private variables to track timer state
    private float currentTime;
    private bool isGameOver = false;
    private bool hasWon = false;

    void Start()
    {
        // Initialize the timer
        currentTime = totalGameTime;

        // Ensure proper UI setup
        if (timerText == null)
        {
            Debug.LogError("Timer Text is not assigned! Please drag a TextMeshProUGUI component to the script.");
        }

        // Hide panels at start
        if (failurePanel != null)
        {
            failurePanel.SetActive(false);
        }
        if (successPanel != null)
        {
            successPanel.SetActive(false);
        }
    }
void Update()
{
    // Only update the timer if the game is not over and the player hasn't won
    if (!isGameOver && !hasWon)
    {
        // Reduce the timer
        currentTime -= Time.deltaTime;

        // Update the timer text
        if (timerText != null)
        {
            // Format the time to show minutes and seconds
            int minutes = Mathf.FloorToInt(currentTime / 60);
            int seconds = Mathf.FloorToInt(currentTime % 60);
            timerText.text = string.Format("{0:00}:{1:00}", minutes, seconds);
        }

        // Check if time has run out
        if (currentTime <= 0)
        {
            EndGame(false); // Call EndGame with a loss if time is out
        }
    }
}

public void CheckWinCondition(bool hasWon)
{
    // If the player has won and the game is still ongoing
    if (hasWon && !isGameOver)
    {
        this.hasWon = true; // Mark the player as having won
        EndGame(true);      // End the game with a win
    }
}

    void EndGame(bool didWin)
    {
        // Mark game as over
        isGameOver = true;

        // Stop game time
        Time.timeScale = 0f;

        if (didWin)
        {
            // Change skeleton system color
            if (skeletonRenderer != null)
            {
                skeletonRenderer.material.color = winColor;
            }

            // Show success panel
            if (successPanel != null)
            {
                successPanel.SetActive(true);
            }
            Debug.Log("You Win! All pieces assembled correctly.");
        }
        else
        {
            // Show failure panel
            if (failurePanel != null)
            {
                failurePanel.SetActive(true);
            }
            Debug.Log("Game Over! Time ran out.");
        }
    }

    // Method to restart the game
    public void RestartGame()
    {
        // Restore normal time flow
        Time.timeScale = 1f;

        // Reload the current scene
        SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex);
    }
}
