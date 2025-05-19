import { useState, useEffect } from 'react';

function App() {
  const [tasks, setTasks] = useState([]);
  const [text, setText] = useState('');

  useEffect(() => {
    fetch('/api/tasks').then(res => res.json()).then(setTasks);
  }, []);

  const addTask = () => {
    fetch('/api/tasks', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text }),
    }).then(() => {
      setText('');
      fetch('/api/tasks').then(res => res.json()).then(setTasks);
    });
  };

  return (
    <div>
      <h1>Tasks</h1>
      <input value={text} onChange={e => setText(e.target.value)} />
      <button onClick={addTask}>Add Task</button>
      <ul>
        {tasks.map((t, i) => <li key={i}>{t.text}</li>)}
      </ul>
    </div>
  );
}

export default App;
