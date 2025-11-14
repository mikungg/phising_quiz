let shuffledQuizData = [];
let flagData = [];

let score = 0;
let flagCounter = 0;

const scoreToWin = 10;

const titleEl = document.getElementById("judul-soal");
const descEl = document.getElementById("deskripsi-soal");
const soalContainerEl = document.getElementById("soal-container");
const soalFrameEl = document.getElementById("soal-iframe");
const scoreEl = document.getElementById("score");
const legitBtn = document.getElementById("legit-btn");
const phishingBtn = document.getElementById("phishing-btn");
const explainModal = new bootstrap.Modal(
  document.getElementById("explainModal"),
  {
    backdrop: "static",
    keyboard: false,
  }
);

const explainModalLabel = document.getElementById("explainModalLabel");
const explainText = document.getElementById("explain-text");
const flagText = document.getElementById("flag-text");
const nextBtn = document.getElementById("next-btn");

function renderQuestion() {
  const q = shuffledQuizData[0];
  titleEl.textContent = q.judul;
  descEl.textContent = q.deskripsi;
  soalFrameEl.src = q.soalHtml;

  scoreEl.textContent = `${score}/${scoreToWin}`;
}

function handleAnswer(choice) {
  const q = shuffledQuizData[0];
  const correct = q.jawaban.toLowerCase();
  const isCorrect = choice === correct;

  if (isCorrect) {
    explainText.textContent = "Benar! " + q.penjelasan;
    explainModalLabel.textContent = "Benar! ";
    flagText.textContent = "Flag: " + flagData[flagCounter];
    nextBtn.textContent = "Next";

    flagCounter++;
    score++;

    shuffledQuizData.shift(); // remove the current question
  } else {
    explainText.textContent = "Salah. " + q.penjelasan;
    explainModalLabel.textContent = "Salah. ";
    flagText.textContent = "";
    nextBtn.textContent = "Coba Lagi";

    shuffledQuizData.shift(); // remove the current question
    shuffledQuizData.push(q); // add it to the end
  }

  explainModal.show();
}

legitBtn.addEventListener("click", () => handleAnswer("legit"));
phishingBtn.addEventListener("click", () => handleAnswer("phishing"));

nextBtn.addEventListener("click", () => {
  explainModal.hide();
  flagText.textContent = "";

  if (score >= scoreToWin) {
    // finished
    titleEl.textContent = "Anda telah menyelesaikan Phishing Quiz";
    scoreEl.textContent = `${score}/${scoreToWin}`;
    descEl.textContent = `${score}/${scoreToWin}`;

    // button hiddden
    legitBtn.hidden = true;
    phishingBtn.hidden = true;
    legitBtn.disabled = true;
    phishingBtn.disabled = true;

    // soal container hidden
    soalContainerEl.className = "col-md-12 my-3 fs-1";
    soalContainerEl.textContent = "Terima kasih telah berpartisipasi!";
    soalContainerEl.style.height = "auto";
  } else {
    renderQuestion();
  }
});

// Fetch shuffled quiz data and flag data from Flask API and initialize
async function initQuiz() {
  try {
    const [quizResponse, flagResponse] = await Promise.all([
      fetch("/api/quiz-data", {
        method: "GET",
        headers: {
          "Accept": "application/json",
        },
        credentials: "same-origin"
      }),
      fetch("/api/flag-data", {
        method: "GET",
        headers: {
          "Accept": "application/json",
        },
        credentials: "same-origin"
      })
    ]);

    if (!quizResponse.ok) {
      throw new Error(`Quiz data fetch failed: ${quizResponse.status}`);
    }
    if (!flagResponse.ok) {
      throw new Error(`Flag data fetch failed: ${flagResponse.status}`);
    }

    const quizData = await quizResponse.json();
    const flags = await flagResponse.json();

    // Validate data structure
    if (!Array.isArray(quizData) || quizData.length === 0) {
      throw new Error("Invalid quiz data format");
    }
    if (!Array.isArray(flags) || flags.length === 0) {
      throw new Error("Invalid flag data format");
    }

    // Validate each quiz item has required fields
    const isValidQuiz = quizData.every(q => 
      q.judul && q.deskripsi && q.soalHtml && q.jawaban && q.penjelasan
    );
    if (!isValidQuiz) {
      throw new Error("Quiz data missing required fields");
    }

    shuffledQuizData = quizData;
    flagData = flags;
    renderQuestion();
  } catch (error) {
    console.error("Error loading quiz:", error);
    // Show user-friendly error message
    titleEl.textContent = "Error Loading Quiz";
    descEl.textContent = "Gagal memuat quiz. Silakan refresh halaman atau hubungi administrator.";
    soalContainerEl.style.display = "none";
    legitBtn.disabled = true;
    phishingBtn.disabled = true;
  }
}

// init
initQuiz();
