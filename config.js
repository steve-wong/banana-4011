const CONFIG = {
  // Game structure
  totalRounds: 10,

  // Timer
  timerDefault: 4,   // seconds
  timerMin: 1,       // seconds
  timerMax: 10,      // seconds

  // Review pause (ms to show the correct answer before advancing; only used in auto-continue mode)
  reviewMs: 3000,

  // Whether to auto-advance after reviewMs (true) or wait for the player to click Continue (false)
  autoContinue: true,

  // Scoring
  pointsCorrect: 10,
  streakBonus: 5,      // extra points per correct answer when streak >= streakThreshold
  streakThreshold: 3,  // minimum streak length to earn the bonus
};
