const CONFIG = {
  // Game structure
  totalRounds: 10,

  // Timer
  timerDefault: 4,   // seconds
  timerMin: 1,       // seconds
  timerMax: 10,      // seconds

  // Review pause (ms to show the correct answer before advancing)
  reviewMs: 3000,

  // Scoring
  pointsCorrect: 10,
  streakBonus: 5,      // extra points per correct answer when streak >= streakThreshold
  streakThreshold: 3,  // minimum streak length to earn the bonus
};
