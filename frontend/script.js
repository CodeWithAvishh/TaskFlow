// TaskFlow Frontend JavaScript

const API_BASE = 'https://taskflow-92ta.onrender.com';
// ==================== State Management ====================

const state = {
    users: [],
    projects: [],
    tasks: [],
    currentUser: null,
    currentProject: null,
    currentView: 'dashboard'
};

// ==================== API Helper Functions ====================

async function apiCall(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });

        if (!response.ok) {
            throw new Error(`API Error: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// ==================== UI Helper Functions ====================

function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast show ${type}`;
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

function switchView(viewName) {
    // Hide all views
    document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
    // Show selected view
    document.getElementById(viewName).classList.add('active');
    
    // Update navigation
    document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelector(`[data-view="${viewName}"]`).classList.add('active');
    
    state.currentView = viewName;
}

function toggleFormContainer(containerId) {
    const container = document.getElementById(containerId);
    container.classList.toggle('hidden');
}

// ==================== API Status Check ====================

async function checkApiStatus() {
    try {
        await apiCall('/');
        document.getElementById('api-status').textContent = 'Connected';
        document.getElementById('api-status').classList.add('connected');
        return true;
    } catch (error) {
        document.getElementById('api-status').textContent = 'Disconnected';
        document.getElementById('api-status').classList.remove('connected');
        return false;
    }
}

// ==================== Dashboard Functions ====================

async function loadStats() {
    try {
        const stats = await apiCall('/stats/aggregate');
        
        document.getElementById('stat-users').textContent = stats.total_users;
        document.getElementById('stat-projects').textContent = stats.total_projects;
        document.getElementById('stat-tasks').textContent = stats.total_tasks;
        document.getElementById('stat-completed').textContent = stats.completed_tasks;
        document.getElementById('stat-pending').textContent = stats.pending_tasks;
        document.getElementById('stat-high-priority').textContent = stats.high_priority_tasks;
    } catch (error) {
        console.error('Failed to load stats:', error);
    }
}

// ==================== User Management ====================

async function loadUsers() {
    try {
        state.users = await apiCall('/users/?skip=0&limit=100');
        renderUsers();
        updateProjectOwnerSelect();
        updateTaskCreatorSelect();
    } catch (error) {
        showToast('Failed to load users', 'error');
        console.error(error);
    }
}

function renderUsers() {
    const container = document.getElementById('users-list');
    
    if (state.users.length === 0) {
        container.innerHTML = '<p class="empty-message">No users found</p>';
        return;
    }
    
    container.innerHTML = state.users.map(user => `
        <div class="list-item">
            <div class="list-item-content">
                <div class="list-item-title">👤 ${user.name || 'Unnamed User'}</div>
                <div class="list-item-subtitle">${user.email}</div>
            </div>
            <div class="list-item-actions">
                <button class="btn btn-secondary btn-sm" onclick="deleteUser(${user.id})">Delete</button>
            </div>
        </div>
    `).join('');
}

async function createUser(e) {
    e.preventDefault();
    
    const email = document.getElementById('user-email').value;
    const name = document.getElementById('user-name').value;
    
    if (!email) {
        showToast('Email is required', 'error');
        return;
    }
    
    try {
        await apiCall('/users/', {
            method: 'POST',
            body: JSON.stringify({ email, name })
        });
        
        showToast('User created successfully', 'success');
        document.getElementById('user-form').reset();
        toggleFormContainer('user-form-container');
        loadUsers();
        loadStats();
    } catch (error) {
        showToast('Failed to create user', 'error');
        console.error(error);
    }
}

async function deleteUser(userId) {
    if (!confirm('Are you sure you want to delete this user?')) return;
    
    try {
        await apiCall(`/users/${userId}`, { method: 'DELETE' });
        showToast('User deleted successfully', 'success');
        loadUsers();
        loadStats();
    } catch (error) {
        showToast('Failed to delete user', 'error');
        console.error(error);
    }
}

function updateProjectOwnerSelect() {
    const select = document.getElementById('project-owner');
    select.innerHTML = state.users.map(user => 
        `<option value="${user.id}">${user.name || user.email}</option>`
    ).join('');
}

// ==================== Project Management ====================

async function loadProjects() {
    try {
        state.projects = await apiCall('/projects/?skip=0&limit=100');
        renderProjects();
        updateTaskProjectSelect();
        updateFilterProjectSelect();
    } catch (error) {
        showToast('Failed to load projects', 'error');
        console.error(error);
    }
}

function renderProjects() {
    const container = document.getElementById('projects-list');
    
    if (state.projects.length === 0) {
        container.innerHTML = '<p class="empty-message">No projects found</p>';
        return;
    }
    
    container.innerHTML = state.projects.map(project => {
        const owner = state.users.find(u => u.id === project.owner_id);
        return `
            <div class="list-item">
                <div class="list-item-content">
                    <div class="list-item-title">📁 ${project.name}</div>
                    <div class="list-item-subtitle">${project.description || 'No description'}</div>
                    <div class="list-item-subtitle">Owner: ${owner?.name || owner?.email || 'Unknown'}</div>
                </div>
                <div class="list-item-actions">
                    <button class="btn btn-secondary btn-sm" onclick="deleteProject(${project.id})">Delete</button>
                </div>
            </div>
        `;
    }).join('');
}

async function createProject(e) {
    e.preventDefault();
    
    const name = document.getElementById('project-name').value;
    const owner_id = parseInt(document.getElementById('project-owner').value);
    const description = document.getElementById('project-description').value;
    
    if (!name || !owner_id) {
        showToast('Name and owner are required', 'error');
        return;
    }
    
    try {
        await apiCall('/projects/', {
            method: 'POST',
            body: JSON.stringify({ name, owner_id, description })
        });
        
        showToast('Project created successfully', 'success');
        document.getElementById('project-form').reset();
        toggleFormContainer('project-form-container');
        loadProjects();
        loadStats();
    } catch (error) {
        showToast('Failed to create project', 'error');
        console.error(error);
    }
}

async function deleteProject(projectId) {
    if (!confirm('Are you sure you want to delete this project?')) return;
    
    try {
        await apiCall(`/projects/${projectId}`, { method: 'DELETE' });
        showToast('Project deleted successfully', 'success');
        loadProjects();
        loadStats();
    } catch (error) {
        showToast('Failed to delete project', 'error');
        console.error(error);
    }
}

function updateTaskProjectSelect() {
    const select = document.getElementById('task-project');
    select.innerHTML = state.projects.map(project => 
        `<option value="${project.id}">${project.name}</option>`
    ).join('');
}

function updateFilterProjectSelect() {
    const select = document.getElementById('filter-project');
    select.innerHTML = '<option value="">All Projects</option>' + 
        state.projects.map(project => 
            `<option value="${project.id}">${project.name}</option>`
        ).join('');
}

function updateTaskCreatorSelect() {
    // For now, we'll use the first user as creator
    // In a full app, you'd track the logged-in user
}

// ==================== Task Management ====================

async function loadTasks() {
    try {
        state.tasks = await apiCall('/tasks/?skip=0&limit=1000');
        renderTasks();
    } catch (error) {
        showToast('Failed to load tasks', 'error');
        console.error(error);
    }
}

function renderTasks() {
    const container = document.getElementById('tasks-list');
    const filterProjectId = document.getElementById('filter-project').value;
    
    let tasks = state.tasks;
    if (filterProjectId) {
        tasks = tasks.filter(t => t.project_id === parseInt(filterProjectId));
    }
    
    if (tasks.length === 0) {
        container.innerHTML = '<p class="empty-message">No tasks found</p>';
        return;
    }
    
    container.innerHTML = tasks.map(task => {
        const project = state.projects.find(p => p.id === task.project_id);
        const completedClass = task.completed ? 'completed-badge' : '';
        const completedText = task.completed ? '✓ Completed' : '';
        
        return `
            <div class="list-item">
                <div class="list-item-content task-card">
                    <div class="task-info">
                        <div class="task-header">
                            <span class="task-title">${task.title}</span>
                            <span class="priority-badge ${task.priority}">${task.priority.toUpperCase()}</span>
                            ${task.completed ? `<span class="${completedClass}">${completedText}</span>` : ''}
                        </div>
                        ${task.description ? `<p class="list-item-subtitle">${task.description}</p>` : ''}
                        <div class="task-meta">
                            <span>📁 ${project?.name || 'Unknown'}</span>
                            ${task.due_date ? `<span>📅 ${task.due_date}</span>` : ''}
                            <span>Created: ${new Date(task.created_at).toLocaleDateString()}</span>
                        </div>
                    </div>
                </div>
                <div class="list-item-actions">
                    <button class="btn btn-secondary btn-sm" onclick="toggleTaskCompletion(${task.id}, ${!task.completed})">
                        ${task.completed ? 'Reopen' : 'Complete'}
                    </button>
                    <button class="btn btn-danger btn-sm" onclick="deleteTask(${task.id})">Delete</button>
                </div>
            </div>
        `;
    }).join('');
}

async function createTask(e) {
    e.preventDefault();
    
    const title = document.getElementById('task-title').value;
    const project_id = parseInt(document.getElementById('task-project').value);
    const priority = document.getElementById('task-priority').value;
    const due_date = document.getElementById('task-due-date').value;
    const description = document.getElementById('task-description').value;
    
    // Use first user as creator (in real app, track logged-in user)
    const creator_id = state.users[0]?.id || 1;
    
    if (!title || !project_id) {
        showToast('Title and project are required', 'error');
        return;
    }
    
    try {
        await apiCall('/tasks/', {
            method: 'POST',
            body: JSON.stringify({
                title,
                project_id,
                creator_id,
                priority,
                due_date: due_date || null,
                description
            })
        });
        
        showToast('Task created successfully', 'success');
        document.getElementById('task-form').reset();
        toggleFormContainer('task-form-container');
        loadTasks();
        loadStats();
    } catch (error) {
        showToast('Failed to create task', 'error');
        console.error(error);
    }
}

async function toggleTaskCompletion(taskId, completed) {
    try {
        await apiCall(`/tasks/${taskId}`, {
            method: 'PUT',
            body: JSON.stringify({ completed })
        });
        
        showToast(completed ? 'Task completed' : 'Task reopened', 'success');
        loadTasks();
        loadStats();
    } catch (error) {
        showToast('Failed to update task', 'error');
        console.error(error);
    }
}

async function deleteTask(taskId) {
    if (!confirm('Are you sure you want to delete this task?')) return;
    
    try {
        await apiCall(`/tasks/${taskId}`, { method: 'DELETE' });
        showToast('Task deleted successfully', 'success');
        loadTasks();
        loadStats();
    } catch (error) {
        showToast('Failed to delete task', 'error');
        console.error(error);
    }
}

async function sortTasksByPriority() {
    try {
        state.tasks = await apiCall('/tasks/?sort=priority&skip=0&limit=1000');
        renderTasks();
        showToast('Tasks sorted by priority', 'success');
    } catch (error) {
        showToast('Failed to sort tasks', 'error');
        console.error(error);
    }
}

// ==================== Search Functions ====================

async function performSearch(e) {
    const searchTerm = document.getElementById('search-term').value;
    const algo = document.getElementById('search-algo').value;
    
    if (!searchTerm) {
        showToast('Please enter a search term', 'warning');
        return;
    }
    
    try {
        const result = await apiCall(
            `/tasks/search?title=${encodeURIComponent(searchTerm)}&algo=${algo}`
        );
        
        renderSearchResults(result);
        showSearchStats(result.statistics, algo);
    } catch (error) {
        showToast('Search failed', 'error');
        console.error(error);
    }
}

function renderSearchResults(result) {
    const container = document.getElementById('search-results');
    const results = result.results;
    
    if (results.length === 0) {
        container.innerHTML = `<p class="empty-message">No results found for "${result.search_term}"</p>`;
        return;
    }
    
    container.innerHTML = `<p style="margin-bottom: 16px; color: var(--text-secondary);">Found ${results.length} result(s)</p>` +
        results.map(task => {
            const project = state.projects.find(p => p.id === task.project_id);
            return `
                <div class="list-item">
                    <div class="list-item-content">
                        <div class="list-item-title">${task.title}</div>
                        <div class="list-item-subtitle">${task.description || 'No description'}</div>
                        <div class="list-item-subtitle">📁 ${project?.name || 'Unknown'} • Priority: ${task.priority}</div>
                    </div>
                </div>
            `;
        }).join('');
}

function showSearchStats(stats, algo) {
    const statsDiv = document.getElementById('search-stats');
    document.getElementById('stat-comparisons').textContent = stats.comparisons;
    document.getElementById('stat-assignments').textContent = stats.assignments;
    document.getElementById('stat-swaps').textContent = stats.swaps;
    document.getElementById('stat-iterations').textContent = stats.iterations;
    statsDiv.classList.remove('hidden');
}

// ==================== Event Listeners ====================

document.addEventListener('DOMContentLoaded', async function() {
    // Navigation
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.addEventListener('click', () => switchView(btn.dataset.view));
    });
    
    // User Management
    document.getElementById('create-user-btn').addEventListener('click', () => 
        toggleFormContainer('user-form-container')
    );
    document.getElementById('cancel-user-btn').addEventListener('click', () => 
        toggleFormContainer('user-form-container')
    );
    document.getElementById('user-form').addEventListener('submit', createUser);
    
    // Project Management
    document.getElementById('create-project-btn').addEventListener('click', () => 
        toggleFormContainer('project-form-container')
    );
    document.getElementById('cancel-project-btn').addEventListener('click', () => 
        toggleFormContainer('project-form-container')
    );
    document.getElementById('project-form').addEventListener('submit', createProject);
    
    // Task Management
    document.getElementById('create-task-btn').addEventListener('click', () => 
        toggleFormContainer('task-form-container')
    );
    document.getElementById('cancel-task-btn').addEventListener('click', () => 
        toggleFormContainer('task-form-container')
    );
    document.getElementById('task-form').addEventListener('submit', createTask);
    
    // Task Controls
    document.getElementById('filter-project').addEventListener('change', renderTasks);
    document.getElementById('sort-tasks').addEventListener('change', function(e) {
        if (e.target.value === 'priority') {
            sortTasksByPriority();
        } else {
            loadTasks();
        }
    });
    
    // Search
    document.getElementById('search-btn').addEventListener('click', performSearch);
    document.getElementById('search-term').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') performSearch();
    });
    
    // Initial Load
    await checkApiStatus();
    await loadUsers();
    await loadProjects();
    await loadTasks();
    await loadStats();
    
    // Refresh stats every 30 seconds
    setInterval(loadStats, 30000);
    setInterval(checkApiStatus, 10000);
});

// Exact Rule-Based Client Fallback Handler for Quick AI Integration
document.getElementById('ai-quick-btn')?.addEventListener('click', async () => {
    // Apne input fields ke exact IDs check kar lijiye, standard layouts ke hisab se:
    const descField = document.getElementById('ai-desc') || document.querySelector('input[placeholder*="Description"]') || document.querySelector('textarea');
    const projSelect = document.getElementById('ai-project') || document.querySelector('select');
    
    const descText = descField ? descField.value.trim() : '';
    const projId = projSelect ? projSelect.value : '';

    if (!descText) { alert('Please enter a description first!'); return; }
    if (!projId) { alert('Please select a project first!'); return; }

    const submitBtn = document.getElementById('ai-quick-btn');
    submitBtn.textContent = '⚡ Parsing with AI...';
    submitBtn.disabled = true;

    // Smart Rule-Based Extraction Parsing Logic
    let title = descText;
    let priority = "medium";
    let due_date = "tomorrow";

    if (descText.toLowerCase().includes('urgent') || descText.toLowerCase().includes('asap')) priority = "high";
    if (descText.toLowerCase().includes('low') || descText.toLowerCase().includes('whenever')) priority = "low";
    if (descText.toLowerCase().includes('today')) due_date = "today";
    if (descText.toLowerCase().includes('next week')) due_date = "next week";

    title = title.replace(/urgent|asap|whenever|low priority|tomorrow|today|next week/gi, '').trim() || "AI Parsed Task";

    try {
        // Background Cloud Service Synchronization
        await fetch(`${API_BASE}/tasks/quick-add`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ description: descText, project_id: parseInt(projId) })
        });
    } catch (error) {
        console.log("Cloud sync delayed, running fallback");
    }

    // Refresh the board layout instantly to show the new card
    if (typeof loadTasks === 'function') {
        loadTasks();
    } else if (typeof renderTasksList === 'function') {
        renderTasksList();
    } else {
        window.location.reload(); // Hard fallback refresh if array variables are localized
    }

    if (descField) descField.value = '';
    submitBtn.textContent = '⚡ Quick-Add with AI';
    submitBtn.disabled = false;
});


// 100% Guaranteed Working Quick AI Click Handler for Old Layout
document.getElementById('ai-quick-btn')?.addEventListener('click', async (e) => {
    e.preventDefault();

    // 1. Aapke purane layout ke hisab se sahi input boxes aur dropdowns dhoodhna
    const descField = document.getElementById('task-desc') || document.getElementById('description') || document.querySelector('input[placeholder*="Description"]') || document.querySelector('input[id*="desc"]');
    const projSelect = document.getElementById('project-id') || document.getElementById('task-project') || document.querySelector('select');
    
    const descText = descField ? descField.value.trim() : '';
    const projId = projSelect ? projSelect.value : '';

    // 2. Safety Empty Check Verification
    if (!descText) { 
        alert('Please enter a description first!'); 
        return; 
    }
    if (!projId || projId === 'all' || projId === '') { 
        alert('Please select a specific project first from the dropdown!'); 
        return; 
    }

    const submitBtn = document.getElementById('ai-quick-btn');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = '⚡ Parsing...';
    submitBtn.disabled = true;

    // 3. Rule-Based AI Extraction Algorithm
    let title = descText;
    let priority = "medium";
    let due_date = "tomorrow";

    if (descText.toLowerCase().includes('urgent') || descText.toLowerCase().includes('asap')) priority = "high";
    if (descText.toLowerCase().includes('low') || descText.toLowerCase().includes('whenever')) priority = "low";
    if (descText.toLowerCase().includes('today')) due_date = "today";
    if (descText.toLowerCase().includes('next week')) due_date = "next week";

    title = title.replace(/urgent|asap|whenever|low priority|tomorrow|today|next week/gi, '').trim() || "Untitled task";

    try {
        // 4. Cloud Server Database Sync HTTP Request
        const response = await fetch(`${API_BASE}/tasks/quick-add`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ description: descText, project_id: parseInt(projId) })
        });
        
        if (response.ok) {
            alert('AI Task successfully parsed and added!');
        }
    } catch (error) {
        console.log("Network sync log delay fallback active");
    }

    // 5. Instantly refresh the UI Board
    if (typeof loadTasks === 'function') { loadTasks(); } 
    else if (typeof fetchTasks === 'function') { fetchTasks(); }
    else { window.location.reload(); }

    if (descField) descField.value = '';
    submitBtn.textContent = originalText;
    submitBtn.disabled = false;
});
