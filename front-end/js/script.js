// script.js

document.addEventListener('DOMContentLoaded', () => {
    const draftStarted = localStorage.getItem('draftStarted');

    // Hide the loader initially
    document.querySelector('#welcomeScreen .loader').style.display = 'none';

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
});

// Event listener for the welcome screen 'Enter' button
document.getElementById('startButton').addEventListener('click', function() {
    // Show the loading spinner
    document.getElementById('loadingSpinner').style.display = 'block';

    // Hide the welcome screen
    document.getElementById('welcomeScreen').style.display = 'none';

    // Initialize the league, then load table data and establish WebSocket connection
    startDraft();
});

function startDraft() {
    fetch('http://localhost:8001/start-draft')
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
    fetch('http://localhost:8001/p/players')
        .then(response => response.json())
        .then(data => {
            populateTable(data);
            setupSocketIO();
        })
        .catch(error => {
            console.error('Error fetching player data:', error);
        });
}

function fetchNominationOrder() {
    fetch('http://localhost:8001/t/get-team-names')
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

// Function to set up Socket.IO (no changes needed)
function setupSocketIO() {
    // Socket.IO client setup
    const socket = io('http://localhost:8001'); // Adjust with your server URL

    // You can also establish your Socket.IO event handlers here
    // Example: socket.on('event', handlerFunction);

    // ... your existing Socket.IO setup code ...
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

document.getElementById('resetButton').addEventListener('click', function() {
    restartDraft();

    if(socket){
        socket.disconnect();
    }
});


function restartDraft() {
    // Clear the localStorage
    localStorage.clear();
    // Reload the page to reset the state
    window.location.reload();
}












// document.addEventListener('DOMContentLoaded', () => {
//     // Fetch data from API
//     fetch('http://localhost:8001/p/players')
//         .then(response => response.json())
//         .then(data => {
//             // Populate the table with the fetched data
//             populateTable(data);
//         })
//         .catch(error => {
//             console.error('Error fetching data:', error);
//         });

//     // Socket.IO client setup
//     const socket = io('http://localhost:8001'); // Adjust with your server URL

    

  
    
// });











// export default {
//     socketResponse: null,
      
//       user_max_bid: 185,
//     // This variable holds the WebSocket endpoint URL
//     WEBSOCKET_ENDPOINT: "ws://web:8001",
//     // This property will hold the WebSocket object once it is instantiated
//     socket: undefined,
//     // This function will be executed when the WebSocket connection is successfully established
//     socketOnOpen: (data) => {
//           console.log('onopen', data);
//       // You might want to call sendEvent here to subscribe or send an initial message
//     },
      
      
//     // This function will be executed when a message is received through the WebSocket connection
//     socketOnMessage: function(message) { // Changed to a function expression
//       let response = JSON.parse(message?.data);
//       if (response.event === 'auction_update') {
//         // Assuming you have state variables for currentBid and highestBidder
//         let currentBid = response.current_bid;
//         let highestBidder = response.highest_bidder;
              
//                // Update the text widget with the current bid
//       CurrentBid_Text.setText("Current Bid: $" + currentBid.toString());
      
//       // If you have a widget to display the highest bidder, update it as well
//       HighestBidder_Text.setText("Highest Bidder: " + highestBidder);
//       } else if (response.event === 'new_round') {
//           // Handle the start of a new round
//           let newPlayer = response.player;
//                   let nominater = response.nominater;
//           this.user_max_bid = response.user_max;
//                   storeValue('nominator', response.nominator);
  
//           // Reset the UI for the new round
//           CurrentBid_Text.setText("Current Bid: $0");
//           HighestBidder_Text.setText("Highest Bidder: " + nominater);
//           NewPlayer_Text.setText("Player on Auction: " + newPlayer); 
//       } else if (response.event === 'prompt_nomination') {
//           // Logic to show the modal or dropdown for player selection
//           showAlert('Nominate a Player', 'info');
//                   // On Page 2
//                   storeValue('isNominationEnabled', true); // Disable nomination after selection
  
//           } else if(response.event === 'error') {
//           showAlert(response.message, 'error');
//       } 
//       console.log("socketOnMessage", response);
//       this.socketResponse = response; // Removed the ?.data since you're already inside the response
//     },
//     // This function will be executed when the WebSocket connection is closed
//     socketOnClose: function(data) { // Changed to a function expression
//       console.log('onclose', data);
//       },
          
          
//     // This asynchronous function is intended to be called when the page loads.
//     // It initializes the WebSocket connection using the provided WEBSOCKET_ENDPOINT
//     // and sets up the event handlers for its onopen, onclose, and onmessage
//     onPageLoad: async function() { // Changed to a function expression
//       this.socket = new WebSocket(this.WEBSOCKET_ENDPOINT);
//           this.socket.onopen = this.socketOnOpen;
//           this.socket.onclose = this.socketOnClose;	
//           this.socket.onmessage = this.socketOnMessage;
//     },
      
//       sendUserBid: function() {
//       // Retrieve the bid amount from the UserBidInput widget
//       let bidAmount = Input1.text
  
//       // Retrieve the current bid from the CurrentBid_Text widget
//       let currentBid = parseInt(CurrentBid_Text.text.replace('$', ''));
  
//       // Retrieve the user's max bid (assuming it's been stored in the UserMaxBid variable)
//       let userMaxBid = this.user_max_bid;
  
//       // Validate the bid amount
//       if (isNaN(bidAmount)) {
//           showAlert('Please enter a valid bid amount.', 'error');
//           return;
//       }
//       if (bidAmount <= currentBid) {
//           showAlert('Your bid must be higher than the current bid.', 'error');
//           return;
//       }
//       if (bidAmount > userMaxBid) {
//           showAlert(`Your bid cannot be higher than your max bid of $${userMaxBid}.`, 'error');
//           return;
//       }
  
//       // If validation passes, send the bid event to the server
//       this.sendEvent("place_human_bid", { amount: bidAmount });
  
//       // Optional: Provide feedback to the user or clear the input field
//       // ...
//       },
      
//           sendNomination: function(selectedPlayer) {
//           this.sendEvent("player_nominated", { player: selectedPlayer });
//           storeValue('isNominationEnabled', false); // Disable nomination after selection
//       },
      
//       startRound: function() {
//       this.sendEvent("start_round");
//       },
  
//       passBid: function() {
//       this.sendEvent("pass_bid");
//       },
  
  
      
//       // Function to send events through the WebSocket connection
//       sendEvent: function(eventType, data) {
//           let eventObj = {
//               event: eventType,
//               data: data,
//               timestamp: Date.now()
//           };
//           this.socket.send(JSON.stringify(eventObj));
//       }
  
    
//   };
  