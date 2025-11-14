// Detect language from URL
const lang = window.location.pathname.includes("/id/") ? "id" : "en";

let shuffledQuizData = [];

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

async function handleAnswer(choice) {
  const q = shuffledQuizData[0];

  // Disable buttons while checking
  legitBtn.disabled = true;
  phishingBtn.disabled = true;

  try {
    // Call Flask API to validate answer
    const response = await fetch(`/api/check-answer/${lang}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      credentials: "same-origin",
      body: JSON.stringify({
        soalHtml: q.soalHtml,
        answer: choice,
      }),
    });

    const result = await response.json();
    const isCorrect = result.isCorrect;

    if (isCorrect) {
      // Fetch the current flag from API
      const flagResponse = await fetch(`/api/get-flag`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        credentials: "same-origin",
        body: JSON.stringify({
          flagCounter: flagCounter,
        }),
      });

      const flagResult = await flagResponse.json();

      if (lang === "id") {
        explainText.textContent = "Benar! " + result.penjelasan;
        explainModalLabel.textContent = "Benar! ";
      } else if (lang === "en") {
        explainText.textContent = "Correct! " + result.penjelasan;
        explainModalLabel.textContent = "Correct! ";
      }

      flagText.textContent = "Flag: " + flagResult.flag;
      nextBtn.textContent = "Next";

      flagCounter++;
      score++;

      shuffledQuizData.shift(); // remove the current question
    } else {
      if (lang === "id") {
        explainText.textContent = "Salah. " + result.penjelasan;
        explainModalLabel.textContent = "Salah. ";
      } else if (lang === "en") {
        explainText.textContent = "Wrong. " + result.penjelasan;
        explainModalLabel.textContent = "Wrong. ";
      }

      flagText.textContent = "";
      nextBtn.textContent = lang === "id" ? "Coba Lagi" : "Try Again";

      shuffledQuizData.shift(); // remove the current question
      shuffledQuizData.push(q); // add it to the end
    }

    explainModal.show();
  } catch (error) {
    console.error("Error checking answer:", error);
    alert("Terjadi kesalahan saat memeriksa jawaban. Silakan coba lagi.");
  } finally {
    // Re-enable buttons
    legitBtn.disabled = false;
    phishingBtn.disabled = false;
  }
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

// Fetch shuffled quiz data from Flask API and initialize
async function initQuiz() {
  const quizResponse = await fetch(`/api/quiz-data/${lang}`, {
    method: "GET",
    headers: {
      Accept: "application/json",
    },
    credentials: "same-origin",
  });

  const quizData = await quizResponse.json();

  shuffledQuizData = quizData;
  renderQuestion();
}

initQuiz();
