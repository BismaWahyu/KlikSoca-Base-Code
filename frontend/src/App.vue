<template>
  <div id="app">
    <!-- Users Section -->
    <div class="users-container">
      <h2>Users</h2>
      <ul id="user-list">
        <li v-for="user in users" :key="user.id">
          {{ user.name }} ({{ user.email }})
          <button @click="editUser(user)">Edit</button>
          <button @click="deleteUser(user.id)">Delete</button>
        </li>
      </ul>
      <form @submit.prevent="createUser" class="user-form">
        <input type="hidden" v-model="form.id">
        <input type="text" v-model="form.name" placeholder="Name" required>
        <input type="email" v-model="form.email" placeholder="Email" required>
        <button type="submit">{{ form.id ? 'Update User' : 'Create User' }}</button>
      </form>
    </div>

    <!-- Playlist Section -->
    <div class="playlist-container">
      <h2>Playlist</h2>
      <ul id="playlist">
        <li v-for="song in playlist" :key="song.id">
          {{ song.title }} - {{ song.artist }}
        </li>
      </ul>
      <form @submit.prevent="addSong" class="song-form">
        <input type="text" v-model="songForm.title" placeholder="Song Title" required>
        <input type="text" v-model="songForm.artist" placeholder="Artist" required>
        <button type="submit">Add Song</button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import io from 'socket.io-client';

const socket = io('http://localhost:5000');

// Users state
const users = ref<any[]>([]);
const form = ref({ id: '', name: '', email: '' });

// Playlist state
const playlist = ref<any[]>([]);
const songForm = ref({ title: '', artist: '' });

// Fetch initial data
const fetchUsers = async () => {
  const response = await fetch('http://localhost:5000/users');
  users.value = await response.json();
};

const fetchPlaylist = async () => {
  const response = await fetch('http://localhost:5000/playlist/songs');
  playlist.value = await response.json();
};

// User functions
const createUser = async () => {
  if (form.value.id) {
    // Update user
    await fetch(`http://localhost:5000/users/${form.value.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: form.value.name, email: form.value.email }),
    });
  } else {
    // Create user
    await fetch('http://localhost:5000/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: form.value.name, email: form.value.email }),
    });
  }
  form.value = { id: '', name: '', email: '' }; // Reset form
};

const editUser = (user: any) => {
  form.value = { ...user };
};

const deleteUser = async (id: string) => {
  await fetch(`http://localhost:5000/users/${id}`, { method: 'DELETE' });
};

// Playlist functions
const addSong = () => {
  socket.emit('add_song', { title: songForm.value.title, artist: songForm.value.artist });
  songForm.value = { title: '', artist: '' }; // Reset form
};

// Lifecycle and Socket.IO listeners
onMounted(() => {
  fetchUsers();
  fetchPlaylist();

  socket.on('new_user', (user: any) => {
    users.value.push(user);
  });

  socket.on('updated_user', (updatedUser: any) => {
    const index = users.value.findIndex(u => u.id === updatedUser.id);
    if (index !== -1) {
      users.value[index] = updatedUser;
    }
  });

  socket.on('deleted_user', (data: any) => {
    users.value = users.value.filter(u => u.id !== data.id);
  });

  socket.on('new_song', (song: any) => {
    playlist.value.push(song);
  });
});
</script>

<style>
#app {
  display: flex;
  justify-content: space-around;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  color: #2c3e50;
  margin-top: 60px;
}

.users-container, .playlist-container {
  width: 45%;
  border: 1px solid #ccc;
  padding: 20px;
  border-radius: 8px;
}

h2 {
  text-align: center;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  padding: 8px;
  margin-bottom: 8px;
  background-color: #f9f9f9;
  border-radius: 4px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.user-form, .song-form {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 20px;
}

input {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  padding: 10px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #369f6e;
}
</style>
