//app.js

const API_URL_USRS = "http://127.0.0.1:8000/api/users"; // Ajusta al endpoint de tu FastAPI
const API_URL_USR = "http://127.0.0.1:8000/api/user"; // Ajusta al endpoint de tu FastAPI
    
    const userForm = document.getElementById("userForm");
    const userId = document.getElementById("userId");
    const nameInput = document.getElementById("name");
    const emailInput = document.getElementById("email");
    const userTable = document.getElementById("userTable");

    // Obtener usuarios
    async function fetchUsers() {
      const res = await axios.get(API_URL_USRS);
      userTable.innerHTML = "";
      res.data.forEach(user => {
        console.log(user.id);
        userTable.innerHTML += `
          <tr>
            <td>${user.id}</td>
            <td>${user.name}</td>
            <td>${user.email}</td>
            <td class="actions">
              <button onclick="editUser(${user.id}, '${user.name}', '${user.email}')">Editar</button>
              <button onclick="deleteUser(${user.id})">Eliminar</button>
            </td>
          </tr>`;
      });
    }

// Crear o actualizar usuario
userForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const data = {};
  if (nameInput.value) data.name = nameInput.value;
  if (emailInput.value) data.email = emailInput.value;

  if (userId.value) {
    await axios.patch(`${API_URL_USR}/${userId.value}`, data);
  } else {
    await axios.post(API_URL_USR, data);
  }
  userForm.reset();
  userId.value = "";
  fetchUsers();
});


    // Editar usuario
    function editUser(id, name, email) {
      userId.value = id;
      nameInput.value = name;
      emailInput.value = email;
    }

    // Eliminar usuario
    async function deleteUser(id) {
      await axios.delete(`${API_URL_USR}/${id}`);
      fetchUsers();
    }

    // Inicial
    fetchUsers();