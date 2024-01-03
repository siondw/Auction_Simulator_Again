// script.js

document.addEventListener('DOMContentLoaded', () => {
    // Fetch data from API
    fetch('http://localhost:8001/p/players')
        .then(response => response.json())
        .then(data => {
            // Populate the table with the fetched data
            populateTable(data);
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });

    // Function to populate the table with player data
    function populateTable(players) {
        const tableBody = document.getElementById('playerTable').getElementsByTagName('tbody')[0];
        tableBody.innerHTML = ''; // Clear the table body

        // Insert new rows
        players.forEach(player => {
            let row = tableBody.insertRow();
            row.innerHTML = `
                <td>${player.name}</td>
                <td>${player.nfl_team}</td>
                <td>${player.pos}</td>
                <td>${player.positional_rank}</td>
                <td>${player.estimated_value}</td>
                <td>${player.projected_points}</td>
                <td><button onclick="nominatePlayer('${player.name}')">Nominate</button></td>
            `;
        });
    }

    // Function to handle player nomination
    function nominatePlayer(playerName) {
        console.log('Player nominated:', playerName);
        // Add logic to handle nomination
    }
    
    // Function to filter the table
function searchTable() {
    const searchInput = document.getElementById('searchInput');
    const filter = searchInput.value.toUpperCase();
    const tbody = document.getElementById('playerTable').getElementsByTagName('tbody')[0];
    const tr = tbody.getElementsByTagName('tr');

    // Loop through all table rows and hide those that don't match the search query
    for (let i = 0; i < tr.length; i++) {
        let td = tr[i].getElementsByTagName("td")[0]; // Change the index if you want to search in another column
        if (td) {
            let txtValue = td.textContent || td.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}

    // Attach search function to search input
    document.getElementById('searchInput').addEventListener('keyup', searchTable);
});








