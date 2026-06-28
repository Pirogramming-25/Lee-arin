// 게임 상태
let attempts = 9;
let strikeCnt = 0;
let ballCnt = 0;

// DOM 요소
const attemptsSpan = document.querySelector('#attempts');
const submitBtn = document.querySelector('.submit-button');
const inputs = document.querySelectorAll('.input-field');
const results = document.querySelector('#results');
const resultImg = document.querySelector('#game-result-img');

// 랜덤 정답 숫자 3개 생성
function getRandom(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}
const numbers = [];
console.log(numbers);
for (let i = 0; i < 3; i++) {
  numbers.push(getRandom(0, 9));
}

// 화면 갱신
function updateUI() {
  attemptsSpan.textContent = attempts;
  for (let i = 0; i < 3; i++) {
    inputs[i].value = '';
  }
}

// 초기 갱신
updateUI();

function check_numbers() {
  // 1. 빈 칸 검사 
  let allFilled = true;
  for (let i = 0; i < 3; i++) {
    if (inputs[i].value === '') {
      allFilled = false;
      break;
    }
  }
  if (!allFilled) return;

  // 2.카운트 리셋
  strikeCnt = 0;
  ballCnt = 0;

  // 3.입력숫자 저장
  let guessStr = '';
  for (let i = 0; i < 3; i++) {
    guessStr += inputs[i].value + ' ';
  }

// 4. 숫자판정
for (let i = 0; i < 3; i++) {
  const guess = Number(inputs[i].value);

  if (guess == numbers[i]) {
    strike();
  } else {
    for (let j = 0; j < 3; j++) {
      if (j !== i && guess == numbers[j]) {
        ball();
        break;                  
      }
    }
  }
}  


  attempts -= 1;

  showResult(guessStr);

  // 7.승패 판정
  if (strikeCnt === 3) {
    resultImg.src = './sucess.png';  
    submitBtn.style.border="2px solid black"
  } else if (attempts === 0) {
    resultImg.src = './fail.png'; 
    submitBtn.style.border="2px solid black"
  }

  updateUI();
}

// 결과 한 줄을 만들어 화면에 추가
function showResult(guessStr) {
  const row = document.createElement('div');
  row.classList.add('check-result');

  // 왼쪽: 입력한 숫자
  const left = document.createElement('span');
  left.classList.add('left');
  left.textContent = guessStr;

  // 가운데: 콜론
  const colon = document.createElement('span');
  colon.textContent = ':';

  // 오른쪽: 결과
  const right = document.createElement('span');
  right.classList.add('right');

  if (strikeCnt === 0 && ballCnt === 0) {
    // 아웃
    const o = document.createElement('span');
    o.classList.add('num-result', 'out');
    o.textContent = 'O';
    right.appendChild(o);
  } else {
    // 스트라이크
    const s = document.createElement('span');
    s.classList.add('num-result', 'strike');
    s.textContent = 'S';

    // 볼
    const b = document.createElement('span');
    b.classList.add('num-result', 'ball');
    b.textContent = 'B';

    right.append(strikeCnt + ' ', s, ' ' + ballCnt + ' ', b);
  }

  row.append(left, colon, right);
  results.appendChild(row);
}

function strike() {
  strikeCnt++;
}

function ball() {
  ballCnt++;
}