function getCsrfToken() {
  return document.cookie.split("; ").find(c => c.startsWith("csrftoken="))?.split("=")[1];
}

async function postJSON(url, body = {}) {
  const res = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCsrfToken(),
    },
    body: JSON.stringify(body),
  });
  return res.json();
}

// 좋아요 토글
document.querySelectorAll(".like-btn").forEach(btn => {
  btn.addEventListener("click", async () => {
    const data = await postJSON(btn.dataset.url);
    btn.classList.toggle("liked", data.liked);
    btn.closest(".post-body").querySelector(".like-count span").textContent = data.like_count;
  });
});

// 댓글 작성
document.querySelectorAll(".comment-form").forEach(form => {
  form.addEventListener("submit", async e => {
    e.preventDefault();
    const input = form.querySelector("input[name=content]");
    const content = input.value.trim();
    if (!content) return;

    const data = await postJSON(form.dataset.url, { content });
    const li = document.createElement("li");
    li.dataset.commentId = data.id;
    li.dataset.updateUrl = `/comments/${data.id}/update/`;
    li.dataset.deleteUrl = `/comments/${data.id}/delete/`;
    li.innerHTML = `<strong>${data.author}</strong> <span class="comment-content"></span>
      <button class="comment-edit">수정</button>
      <button class="comment-delete">삭제</button>`;
    li.querySelector(".comment-content").textContent = data.content;
    bindCommentEvents(li);
    form.closest(".post-body").querySelector(".comment-list").appendChild(li);
    input.value = "";
  });
});

// 댓글 수정/삭제
function bindCommentEvents(li) {
  li.querySelector(".comment-edit")?.addEventListener("click", async () => {
    const span = li.querySelector(".comment-content");
    const newContent = prompt("댓글 수정", span.textContent);
    if (newContent === null || !newContent.trim()) return;
    const data = await postJSON(li.dataset.updateUrl, { content: newContent.trim() });
    span.textContent = data.content;
  });

  li.querySelector(".comment-delete")?.addEventListener("click", async () => {
    if (!confirm("댓글을 삭제할까요?")) return;
    const data = await postJSON(li.dataset.deleteUrl);
    if (data.deleted) li.remove();
  });
}
document.querySelectorAll(".comment-list li").forEach(bindCommentEvents);

// 팔로우 토글
const followBtn = document.getElementById("follow-btn");
followBtn?.addEventListener("click", async () => {
  const data = await postJSON(followBtn.dataset.url);
  followBtn.classList.toggle("following", data.is_following);
  followBtn.textContent = data.is_following ? "팔로잉" : "팔로우";
  document.getElementById("follower-count").textContent = data.follower_count;
});

// 스토리 뷰어
const viewer = document.getElementById("story-viewer");
if (viewer) {
  const imgs = viewer.querySelectorAll(".story-img");
  const bars = viewer.querySelectorAll(".story-progress .bar");
  let current = 0;

  function show(index) {
    current = Math.max(0, Math.min(index, imgs.length - 1));
    imgs.forEach((img, i) => img.classList.toggle("active", i === current));
    bars.forEach((bar, i) => bar.classList.toggle("seen", i <= current));
  }
  show(0);

  viewer.querySelector(".prev").addEventListener("click", () => show(current - 1));
  viewer.querySelector(".next").addEventListener("click", () => show(current + 1));
}
