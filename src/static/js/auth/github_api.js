document.addEventListener('DOMContentLoaded', function() {
    const githubUsernameInput = document.querySelector('#githubUsername');
    const resultsList = document.querySelector('#resultsList');
    const searchButton = document.querySelector('#searchButton');

    function searchGitHubUsers(username) {
        resultsList.classList.add('border-gray-400');

        fetch(`https://api.github.com/search/users?q=${username}`)
            .then(response => response.json())
            .then(data => {
                resultsList.innerHTML = '';
                data.items.slice(0, 3).forEach(user => {
                    const li = document.createElement('li');
                    li.innerHTML = `<a href="#" class="block px-4 py-2 hover:bg-gray-200">${user.login}</a>`;
                    li.addEventListener('click', function(event) {
                        event.preventDefault();
                        githubUsernameInput.value = user.login;
                        resultsList.innerHTML = '';
                    });
                    resultsList.appendChild(li);
                });
            })
            .catch(error => {
                console.error('Erro ao buscar usuários do GitHub:', error);
                resultsList.innerHTML = '<li class="px-4 py-2 text-red-500">Erro ao buscar usuários do GitHub.</li>';
            });
    }

    githubUsernameInput.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            const inputValue = this.value.trim();
            inputValue.length > 0
                ? searchGitHubUsers(inputValue)
                : resultsList.innerHTML = '';
        }
    });

    searchButton.addEventListener('click', function() {
        const inputValue = githubUsernameInput.value.trim();
        inputValue.length > 0
            ? searchGitHubUsers(inputValue)
            : resultsList.innerHTML = '';
    });
});
