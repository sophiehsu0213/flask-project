async function loadItems() {
  const res = await fetch("/items");
  const items = await res.json();

  const ul = document.getElementById("list");
  ul.innerHTML = "";

  items.forEach(i => {
    const li = document.createElement("li");
    li.textContent = i.id + ": " + i.name;

    const btn = document.createElement("button");
    btn.textContent = "Delete";
    btn.onclick = async () => {
      await fetch("/items/" + i.id, { method: "DELETE" });
      loadItems();
    };

    li.appendChild(btn);
    ul.appendChild(li);
  });
}

async function addItem() {
  const input = document.getElementById("nameInput");
  if (!input.value) return;

  await fetch("/items", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name: input.value })
  });

  input.value = "";
  loadItems();
}

loadItems();
