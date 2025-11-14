// English quiz script
const quizDataEn = [
  {
    title: "Sample Email 1",
    description: "The email asks you to update your password via a link.",
    image: "../assets/image/phishing1.png",
    answer: "phishing",
    explanation:
      "The link is not an official domain and asks for credentials — signs of phishing.",
  },
  {
    title: "Sample Email 2",
    description: "An email from a colleague with an unexpected attachment.",
    image: "../assets/image/phishing2.png",
    answer: "legit",
    explanation:
      "The sender is known and the context fits. Still, confirm with the sender when unsure.",
  },
];

let current = 0;
let score = 0;

const titleEl = document.getElementById("judul-soal");
const descEl = document.getElementById("deskripsi-soal");
const imgEl = document.getElementById("image-soal");
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
const explainText = document.getElementById("explain-text");
const nextBtn = document.getElementById("next-btn");

function renderQuestion() {
  const q = quizDataEn[current];
  titleEl.textContent = q.title;
  descEl.textContent = q.description;
  imgEl.src = q.image;
  scoreEl.textContent = `${score}/${quizDataEn.length}`;
}

function handleAnswer(choice) {
  const q = quizDataEn[current];
  const correct = q.answer.toLowerCase();
  const isCorrect = choice === correct;
  if (isCorrect) score++;
  explainText.textContent =
    (isCorrect ? "Correct! " : "Wrong. ") + q.explanation;
  explainModal.show();
}

legitBtn.addEventListener("click", () => handleAnswer("legit"));
phishingBtn.addEventListener("click", () => handleAnswer("phishing"));

nextBtn.addEventListener("click", () => {
  explainModal.hide();
  current++;
  if (current >= quizDataEn.length) {
    titleEl.textContent = "Finished";
    descEl.textContent = `Final score: ${score}/${quizDataEn.length}`;
    imgEl.src = "../assets/image/finished.png";
    legitBtn.disabled = true;
    phishingBtn.disabled = true;
    scoreEl.textContent = `${score}/${quizDataEn.length}`;
  } else {
    renderQuestion();
  }
});

renderQuestion();
