const API = "http://localhost:5000";


async function loadTasks() {
const res = await fetch(`${API}/tasks`);
const tasks = await res.json();
const list = document.getElementById("tasks");
list.innerHTML = "";


tasks.forEach(t => {
const li = document.createElement("li");
li.innerHTML = `${t.title} <button onclick="deleteTask(${t.id})">X</button>`;
list.appendChild(li);
});
}


async function addTask() {
const title = document.getElementById("taskInput").value;
await fetch(`${API}/tasks`, {
method: 'POST',
headers: { 'Content-Type': 'application/json' },
body: JSON.stringify({ title })
});
loadTasks();
}


async function deleteTask(id) {
await fetch(`${API}/tasks/${id}`, { method: 'DELETE' });
loadTasks();
}


loadTasks();