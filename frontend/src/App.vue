<template>
  <div id="app" class="w-full flex gap-3 p-6">
    <!-- Users Section -->
    <div class="w-1/2 drop-shadow">
      <Card>
        <CardHeader>
          <CardTitle>User Management</CardTitle>
          <CardDescription>Manage all users here</CardDescription>
        </CardHeader>
        <CardContent>
          <Card class="p-3">
            <ul id="user-list">
              <li v-for="user in users" :key="user.id">
                <div class="flex justify-between mb-3 items-center">
                  <div class="flex-col flex">
                    <span class="text-lg font-semibold">
                      {{ user.name }} 
                    </span>
                    <span class="text-zinc-500">({{ user.email }})</span>
                  </div>
                  <div class="flex justify-between gap-2">
                    <Button @click="editUser(user)" class="bg-blue-500 hover:bg-blue-600 text-white cursor-pointer">
                      <Pen />
                    </Button>
                    <Button @click="deleteUser(user.id)" class="bg-red-500 hover:bg-red-600 text-white cursor-pointer">
                      <Trash />
                    </Button>
                  </div>
                </div>
              </li>
            </ul>
          </Card>
        </CardContent>
        <CardFooter class="flex gap-2 justify-between items-end">
          <div class="flex flex-col gap-2">
            <Label>Name</Label>
            <Input v-model="form.name" required type="text" placeholder="type your name..." />
          </div>
          <div class="flex flex-col gap-2">
            <Label>Email</Label>
            <Input v-model="form.email" required type="email" placeholder="type your email..." />
          </div>
          <div>
            <Button class="bg-green-500 text-white hover:bg-green-600 cursor-pointer" @click="createUser">Submit</Button>
          </div>
        </CardFooter>
      </Card>
    </div>

    <div class="w-1/2 drop-shadow">
      <Card>
        <CardHeader>
          <CardTitle>Playlist Management</CardTitle>
          <CardDescription>Manage current playlist here</CardDescription>
        </CardHeader>
        <CardContent>
          <Card class="p-3">
            <ul id="playlist">
              <li v-for="song in playlist" :key="song.id">
                <div class="flex justify-between mb-3 items-center">
                  <div class="flex-col flex">
                    <span class="text-lg font-semibold">
                      {{ song.title }} 
                    </span>
                    <span class="text-zinc-500">({{ song.artist }})</span>
                  </div>
                </div>
              </li>
            </ul>
          </Card>
        </CardContent>
        <CardFooter class="flex gap-2 justify-between items-end">
          <div class="flex flex-col gap-2">
            <Label>Song Title</Label>
            <Input v-model="songForm.title" required type="text" placeholder="Title here..." />
          </div>
          <div class="flex flex-col gap-2">
            <Label>Artist</Label>
            <Input v-model="songForm.artist" required type="text" placeholder="Artist here..." />
          </div>
          <div>
            <Button class="bg-green-500 text-white hover:bg-green-600 cursor-pointer" @click="addSong">Add Song</Button>
          </div>
        </CardFooter>
      </Card>
    </div>

    <!-- Notification -->
    <div v-if="showNotification" class="notification">
      {{ notificationMessage }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import io from 'socket.io-client';
import { Trash, Pen } from 'lucide-vue-next';
import { 
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle
} from './components/ui/card';
import { Button } from './components/ui/button';
import { Label } from './components/ui/label'
import { Input } from './components/ui/input';

const socket = io('http://localhost:5000');

// Users state
const users = ref<any[]>([]);
const form = ref({ id: '', name: '', email: '' });

// Playlist state
const playlist = ref<any[]>([]);
const songForm = ref({ title: '', artist: '' });

// Notification state
const showNotification = ref(false);
const notificationMessage = ref('');

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
  form.value = { id: '', name: '', email: '' };
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

    // Show notification
    notificationMessage.value = `New song added: ${song.title} by ${song.artist}`;
    showNotification.value = true;

    // Hide notification after 3 seconds
    setTimeout(() => {
      showNotification.value = false;
    }, 3000);
  });
});
</script>

<style scoped>
.notification {
  position: fixed;
  top: 20px;
  right: 20px;
  background-color: #42b983;
  color: white;
  padding: 15px;
  border-radius: 5px;
  z-index: 1000;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}
</style>
