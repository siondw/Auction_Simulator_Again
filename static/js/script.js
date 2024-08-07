const config = {
    development: 'http://localhost:4000',
    production: 'https://cottage-8ec4da33e7ac.herokuapp.com'
};



const isLocalhost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
const environment = isLocalhost ? 'development' : 'production';
console.log('Environment:', environment);

// Base URL for API requests
const BASE_URL = config[environment];



// script.js
class SocketIOManager {
    constructor() {
        this.socket = io(BASE_URL);
        this.user_max_bid = 186;
        this.session_id = localStorage.getItem('session_id'); // Retrieve the session ID from localStorage
        console.log('Session ID in constructor:', this.session_id); // Add this for debugging
    }

    initialize() {
        this.setupEventHandlers();
    }

    setupEventHandlers() {
        this.socket.on('connect', () => {
            console.log('Connected to the server.');
        });

        this.socket.on('auction_update', (data) => {
            // Example: Update UI elements with received data
            this.updateAuctionUI(data);
        });

        this.socket.on('round_over', () => {
            this.endRound();
        });
        

        this.socket.on('new_round', (data) => {
            // Handle new round logic
            this.handleNewRound(data);
        });

        this.socket.on('prompt_nomination', () => {
            // Handle prompt nomination logic
            this.promptNomination();
        });

        this.socket.on('error', (message) => {
            console.log('Error received:', message);
            showAlert(message, 'error');
        });

        this.socket.on('disconnect', () => {
            console.log('Disconnected from the server.');
        });

    }

    updateAuctionUI(data) {
        const CurrentBid_Text = document.getElementById('currentBid');
        const HighestBidder_Text = document.getElementById('highestBidder');
        const bidButton = document.getElementById('bidButton');

        if (data.highest_bidder === "Team 1") {
            // Add the CSS class 'gray-button' to color the button gray
            bidButton.classList.add('disabled'); 
            // Optionally disable the button after starting the round to prevent multiple clicks
            bidButton.disabled = true;
            
        } else {
            bidButton.classList.remove('disabled'); // Reset the color back to blue
            bidButton.disabled = false; // Enable the button again
        }

        // Update your UI elements here
        // Example:
        CurrentBid_Text.textContent = ("Current Bid: $" + data.current_bid);
        HighestBidder_Text.textContent = ("Highest Bidder: " + data.highest_bidder);

        updateBidInput();
    }

    handleNewRound(data) {
    
        const CurrentBid_Text = document.getElementById('currentBid');
        const HighestBidder_Text = document.getElementById('highestBidder');
        const NewPlayer_Text = document.getElementById('nominatedPlayer');


        // Logic for handling a new round
        
        CurrentBid_Text.textContent = "Current Bid: $" + 1; // Assuming data.currentBid holds the bid value
        HighestBidder_Text.textContent = "Highest Bidder: " + data.nominator;
        NewPlayer_Text.textContent = "Player on Auction: " + data.player;
        this.user_max_bid = data.user_max;
        localStorage.setItem('nominator', data.nominator);

        this.highlightCurrentNominator(data.nominator);
    }

    highlightCurrentNominator(nominator) {
        // Remove highlighting from all teams
        const teams = document.querySelectorAll('#nominationOrderList li');
        teams.forEach(team => {
            team.classList.remove('current-nominator');
        });

        // Strip away "Team " from the nominator string to get the team number
        let teamNumber = nominator.replace('Team ', '');

        // Add highlighting to the current nominator
        const currentNominatorItem = document.getElementById(teamNumber);
        if (currentNominatorItem) {
            currentNominatorItem.classList.add('current-nominator');
            console.log("Applied current-nominator to:", currentNominatorItem);
        }
    }

    promptNomination() {

        const NewPlayer_Text = document.getElementById('nominatedPlayer');
        const draftLogicContainer = document.getElementById('draftLogicContainer');

        draftLogicContainer.classList.add('glowing-gold');

        NewPlayer_Text.textContent = "Your Turn to Nominate a Player!";
        localStorage.setItem('isNominationEnabled', true);
    }

    sendUserBid() {
        const CurrentBid_Text = document.getElementById('currentBid');

        // Retrieve the bid amount from the UserBidInput widget
        let bidAmount = bidInput.value;

        // Retrieve the current bid from the CurrentBid_Text widget
        let currentBid = parseInt(CurrentBid_Text.textContent.replace(/[^0-9]/g, ''));

        // Retrieve the user's max bid (assuming it's been stored in the UserMaxBid variable)
        let userMaxBid = this.user_max_bid;

        // Validate the bid amount
        if (isNaN(bidAmount)) {
            alert('Please enter a valid bid amount.', 'error');
            return;
        }
        if (bidAmount <= currentBid) {
            alert('Your bid must be higher than the current bid.', 'error');
            return;
        }
        if (bidAmount > userMaxBid) {
            alert(`Your bid cannot be higher than your max bid of $${userMaxBid}.`, 'error');
            return;
        }

        // Send the bid to the server
        this.socket.emit('place_human_bid', { session_id: this.session_id, bid_amount: bidAmount });
        console.log("Bid Placed: " + bidAmount);
    }

    sendNomination(selectedPlayer) {
        this.socket.emit("player_nominated", { session_id: this.session_id, player: selectedPlayer });
        draftLogicContainer.classList.remove('glowing-gold');
        localStorage.setItem('isNominationEnabled', false);
    }

    startRound() {
        console.log('Session ID before starting round:', this.session_id);
        this.socket.emit('start_round', { session_id: this.session_id });
    }
    

    passBid() {
        this.socket.emit("pass_bid", { session_id: this.session_id });
    }

    endRound() {
        const CurrentBid_Text = document.getElementById('currentBid');
        const HighestBidder_Text = document.getElementById('highestBidder');
        const NewPlayer_Text = document.getElementById('nominatedPlayer');
        const startRoundButton = document.getElementById('startRound');
        const inputBid = document.getElementById('bidInput');
        const passButton = document.getElementById('passButton');

        CurrentBid_Text.textContent = "Current Bid: "; // Assuming data.currentBid holds the bid value
        
        HighestBidder_Text.textContent = "Highest Bidder: " ;
        NewPlayer_Text.textContent = "Player on Auction: " ;
        inputBid.value = 1;

        fetchPlayersAndSetupApp();
        fetchRoundSummaries();

        startRoundButton.classList.remove('gray-button'); // Reset the color back to blue
        startRoundButton.disabled = false; // Enable the button again
        passButton.classList.remove('gray-button');
        passButton.textContent = "Pass";

    }
}







document.addEventListener('DOMContentLoaded', () => {
    let socket;  // Declare socket variable to be initialized later

    const draftStarted = localStorage.getItem('draftStarted');
    const session_id = localStorage.getItem('session_id');  // Retrieve session ID
    console.log('Session ID on DOMContentLoaded:', session_id);  // Debugging session ID

    if (draftStarted && session_id) {
        // Initialize SocketIOManager with the retrieved session ID
        socket = new SocketIOManager();
        socket.initialize();

        // Hide the welcome screen
        document.getElementById('welcomeScreen').style.display = 'none';
        // Continue with the application setup
        fetchPlayersAndSetupApp();
        fetchNominationOrder();
        fetchRoundSummaries();
    } else {
        // Show the welcome screen
        document.getElementById('welcomeScreen').style.display = 'block';
        // Attach the event listener to the start button
        document.getElementById('startButton').addEventListener('click', () => {
            startDraft().then(() => {
                // Initialize SocketIOManager after session ID is set
                socket = new SocketIOManager();
                socket.initialize();
            });
        });
    }

    // Attach event listener for the "Start Round" button after initialization
    document.getElementById('startRound').addEventListener('click', () => {
        const session_id = localStorage.getItem('session_id');
        console.log('Session ID before starting round:', session_id);  // Debugging session ID

        socket.startRound();
    });

    // Other event listeners...
    document.getElementById('resetButton').addEventListener('click', function() {
        restartDraft();
        if (socket) {
            socket.disconnect();
        }
    });

    document.getElementById('passButton').addEventListener('click', function() {
        const passButton = document.getElementById('passButton');
        passButton.classList.add('gray-button');
        passButton.textContent = "Passed";
        socket.passBid();
    });

    document.getElementById('bidButton').addEventListener('click', function() {
        socket.sendUserBid();
    });

    window.nominatePlayer = function(playerName) {
        socket.sendNomination(playerName);
    };

    openTab(event, 'SearchAndTable');
});


function startDraft() {
    return fetch(`${BASE_URL}/start-draft`)
        .then(response => response.json())
        .then(data => {
            console.log('Draft started:', data.message);
            // Store the session ID in localStorage
            localStorage.setItem('session_id', data.session_id);
            console.log('Session ID set:', data.session_id);  // Debugging session ID

            fetchPlayersAndSetupApp();
            fetchNominationOrder();
        })
        .catch(error => {
            console.error('Error starting draft:', error);
        })
        .finally(() => {
            document.getElementById('welcomeScreen').style.display = 'none';
        });

    localStorage.setItem('draftStarted', true);
    localStorage.setItem('isNominationEnabled', false);
}




function fetchPlayersAndSetupApp() {
    const session_id = localStorage.getItem('session_id');
    
    fetch(`${BASE_URL}/p/players?session_id=${session_id}`)
        .then(response => response.json())
        .then(data => {
            populateTable(data);
        })
        .catch(error => {
            console.error('Error fetching player data:', error);
        });
}

function fetchNominationOrder() {
    fetch(`${BASE_URL}/t/get-team-names?session_id=${localStorage.getItem('session_id')}`)
        .then(response => response.json())
        .then(teamNames => {
            console.log("Received team names:", teamNames); // Add this line to inspect the response
            if (!Array.isArray(teamNames)) {
                console.error("Expected an array of team names but got:", teamNames);
                return;
            }

            const list = document.getElementById('nominationOrderList');
            list.innerHTML = ''; // Clear existing list items

            teamNames.forEach(teamName => {
                const listItem = document.createElement('li');
                listItem.textContent = teamName;
                list.appendChild(listItem);
            });
        })
        .catch(error => {
            console.error('Error fetching nomination order:', error);
        });
}

function fetchRoundSummaries() {
    const session_id = localStorage.getItem('session_id');
    
    fetch(`${BASE_URL}/get-round-summaries/?session_id=${session_id}`)
        .then(response => response.json())
        .then(summaries => {
            const list = document.getElementById('roundSummariesList');
            list.innerHTML = ''; // Clear existing list items

            summaries.forEach(summary => {
                const listItem = document.createElement('li');
                listItem.textContent = summary; // Adjust if summary structure is different
                list.appendChild(listItem);
                scrollToBottom();
            });
        })
        .catch(error => {
            console.error('Error fetching round summaries:', error);
        });
}


function scrollToBottom() {
    const list = document.getElementById('roundSummariesList');
    list.scrollTop = list.scrollHeight;
}




function populateTable(players) {
    console.log("Received players data:", players); // Add this line to inspect the response
    if (!Array.isArray(players)) {
        console.error("Expected an array of players but got:", players);
        return;
    }

    const tableBody = document.getElementById('playerTable').getElementsByTagName('tbody')[0];
    tableBody.innerHTML = ''; // Clear the table body

    // Insert new rows
    players.forEach(player => {
        let row = tableBody.insertRow();
        row.innerHTML = `
            <td><button onclick="window.nominatePlayer('${player.name}')">Nominate</button></td>
            <td>${player.name}</td>
            <td>${player.estimated_value}</td>
            <td>${player.pos}</td>
            <td>${player.positional_rank}</td>
            <td>${player.projected_points}</td>
        `;
    });
}


// Function to filter the table
function searchTable() {
const searchInput = document.getElementById('searchInput');
const filter = searchInput.value.toUpperCase();
const tbody = document.getElementById('playerTable').getElementsByTagName('tbody')[0];
const tr = tbody.getElementsByTagName('tr');

// Loop through all table rows and hide those that don't match the search query
for (let i = 0; i < tr.length; i++) {
    let td = tr[i].getElementsByTagName("td")[1]; // Change the index if you want to search in another column
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

function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    
    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";

    // Lazy load Team Display content
    if (tabName === 'TeamDisplay') {
        updateTeamDisplay('1'); // Load data for Team 1 by default
    } else if (tabName === 'SearchAndTable') {
        filterTableByPosition('All'); // Show all positions by default
    }
}


// Attach search function to search input
document.getElementById('searchInput').addEventListener('keyup', searchTable);

document.getElementById('positionDropdown').addEventListener('change', function() {
    filterTableByPosition(this.value);
});

function filterTableByPosition(position) {
    const table = document.getElementById('playerTable');
    const rows = table.getElementsByTagName('tr');

    for (let i = 1; i < rows.length; i++) { // Start loop from 1 to skip table header
        let td = rows[i].getElementsByTagName('td')[3]; // 4th column for position
        if (td) {
            let cellValue = td.textContent || td.innerText;
            // Show the row if position matches, or if position is 'FLEX' (excluding 'QB'), or if 'All' is selected
            if (position === 'All' || (position === 'FLEX' && cellValue !== 'QB') || cellValue === position) {
                rows[i].style.display = '';
            } else {
                rows[i].style.display = 'none';
            }
        }
    }
}

function setUpButtonHandlers() {
    
}


function updateBidInput() {
    const currentBidSpan = document.getElementById('currentBid');
    const bidInput = document.getElementById('bidInput');

    let currentBid = parseInt(currentBidSpan.textContent.replace(/[^0-9]/g, ''));

    currentInput = currentBid + 1;

    bidInput.value = currentInput;
}

// API call to out get team roster data, that gets a teams' roster based on team ID
function updateTeamDisplay(selectedTeam) {
    if (selectedTeam) {
        fetch(`${BASE_URL}/t/get-team-roster/` + selectedTeam)
            .then(response => response.json())
            .then(rosterData => updateRosterDisplay(rosterData))
            .catch(error => console.error('Error fetching roster data:', error));
    }
}

// Function to update the team roster display
function updateRosterDisplay(rosterData) {
    console.log('Roster data:', rosterData);
    var rosterTable = document.getElementById('rosterTable').getElementsByTagName('tbody')[0];
    rosterTable.innerHTML = ''; // Clear existing rows

    var positions = ['QB1', 'QB2', 'WR1', 'WR2', 'WR3', 'RB1', 'RB2', 'TE1', 'Flex', 'BN1', 'BN2', 'BN3', 'BN4', 'BN5', 'BN6'];

    positions.forEach(position => {
        var row = document.createElement('tr'); // Create a new table row

        var positionCell = document.createElement('td'); // Create a new cell for the position
        positionCell.textContent = position; // Set the cell's text to the position
        row.appendChild(positionCell); // Add the cell to the row

        var playerCell = document.createElement('td'); // Create a new cell for the player
        var player = rosterData.find(player => player.slot === position); // Find the player for this position
        playerCell.textContent = player ? player.name : ''; // Set the cell's text to the player's name if a player is found, or to an empty string if not
        row.appendChild(playerCell); // Add the cell to the row

        rosterTable.appendChild(row); // Add the row to the table
    });
}



function restartDraft() {
    // Clear the localStorage
    localStorage.clear();
    // Reload the page to reset the state
    window.location.reload();
}

