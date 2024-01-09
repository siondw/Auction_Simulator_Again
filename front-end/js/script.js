// script.js
class SocketIOManager {
    constructor() {
        this.socket = io('http://localhost:4000'); // Adjust the URL
        this.user_max_bid = 186;
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
    }

    promptNomination() {
        // Logic to show the modal or dropdown for player selection
        showAlert('Nominate a Player', 'info');
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
        this.socket.emit('place_human_bid', { bid_amount: bidAmount });
        console.log("Bid Placed: " + bidAmount);
    }

    sendNomination(selectedPlayer) {
        this.socket.emit("player_nominated", { player: selectedPlayer });
        localStorage.setItem('isNominationEnabled', false);
    }

    startRound() {
        console.log("Starting Round...")
        this.socket.emit("start_round");
        
    }

    passBid() {
        this.socket.emit("pass_bid");
    }

    endRound() {
        const CurrentBid_Text = document.getElementById('currentBid');
        const HighestBidder_Text = document.getElementById('highestBidder');
        const NewPlayer_Text = document.getElementById('nominatedPlayer');
        const startRoundButton = document.getElementById('startRound');
        const inputBid = document.getElementById('bidInput');

        CurrentBid_Text.textContent = "Current Bid: "; // Assuming data.currentBid holds the bid value
        
        HighestBidder_Text.textContent = "Highest Bidder: " ;
        NewPlayer_Text.textContent = "Player on Auction: " ;
        inputBid.value = 1;

        fetchPlayersAndSetupApp();

        startRoundButton.classList.remove('gray-button'); // Reset the color back to blue
        startRoundButton.disabled = false; // Enable the button again

    }
}







document.addEventListener('DOMContentLoaded', () => {
    const draftStarted = localStorage.getItem('draftStarted');
    const socket = new SocketIOManager();
    socket.initialize();



    if (draftStarted) {
        // Hide the welcome screen
        document.getElementById('welcomeScreen').style.display = 'none';
        // Continue with the application setup
        fetchPlayersAndSetupApp();
        fetchNominationOrder();
    } else {
        // Show the welcome screen
        document.getElementById('welcomeScreen').style.display = 'block';
        // Attach the event listener to the start button
        document.getElementById('startButton').addEventListener('click', startDraft);
    }

        // Get your "Start Round" button by ID
        const startRoundButton = document.getElementById('startRound');

        // Attach an event listener to the "Start Round" button
        startRoundButton.addEventListener('click', () => {
            // Add the CSS class 'gray-button' to color the button gray
            startRoundButton.classList.add('gray-button'); 
            // Optionally disable the button after starting the round to prevent multiple clicks
            startRoundButton.disabled = true;
            
            
            // Call the startRound method when the button is clicked
            socket.startRound();

            
        });

        document.getElementById('resetButton').addEventListener('click', function() {
            restartDraft();
        
            if(socket){
                socket.disconnect();
            }
        });
        
        document.getElementById('passButton').addEventListener('click', function() {
            socket.passBid();
        });

        document.getElementById('bidButton').addEventListener('click', function() {
            socket.sendUserBid();
        });

        
});



function startDraft() {
    fetch('http://localhost:4000/start-draft')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Draft started:', data.message);
        fetchPlayersAndSetupApp();
        fetchNominationOrder();
    })
    .catch(error => {
        console.error('Error starting draft:', error);
    })
    .finally(() => {
        // Hide the loader and the welcome screen after draft starts
        document.getElementById('welcomeScreen').style.display = 'none';
    });

    localStorage.setItem('draftStarted', true);
}


function fetchPlayersAndSetupApp() {
    // Fetch data from API to populate the table
    fetch('http://localhost:4000/p/players')
        .then(response => response.json())
        .then(data => {
            populateTable(data);
        })
        .catch(error => {
            console.error('Error fetching player data:', error);
        });
}

function fetchNominationOrder() {
    fetch('http://localhost:4000/t/get-team-names')
        .then(response => response.json())
        .then(teamNames => {
            const list = document.getElementById('nominationOrderList');
            teamNames.forEach(teamName => {
                const listItem = document.createElement('li');
                listItem.textContent = teamName;

                // Extracting the team number from the team name
                const teamNumber = teamName.split(' ')[1]; // Assuming the format "Team X"
                listItem.id = teamNumber; // Setting the ID as X

                list.appendChild(listItem);
            });
        })
        .catch(error => {
            console.error('Error fetching nomination order:', error);
        });
}



// Function to populate the table with player data
function populateTable(players) {
    const tableBody = document.getElementById('playerTable').getElementsByTagName('tbody')[0];
    tableBody.innerHTML = ''; // Clear the table body

    // Insert new rows
    players.forEach(player => {
        let row = tableBody.insertRow();
        row.innerHTML = `
            <td><button onclick="nominatePlayer('${player.name}')">Nominate</button></td>
            <td>${player.name}</td>
            <td>${player.estimated_value}</td>
            <td>${player.pos}</td>
            <td>${player.positional_rank}</td>
            <td>${player.projected_points}</td>
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


function restartDraft() {
    // Clear the localStorage
    localStorage.clear();
    // Reload the page to reset the state
    window.location.reload();
}

