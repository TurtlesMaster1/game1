// rust_ipc_server.rs
// This is the Rust server program that Python will talk to.

use std::io::{self, Read, Write, BufReader, BufRead};
use std::net::{TcpListener, TcpStream};
use std::thread; // For handling connections in a separate thread
use std::time::Duration;

fn handle_client(mut stream: TcpStream) -> io::Result<()> {
    let peer_addr = stream.peer_addr()?;
    println!("\nRust Server: Client connected: {}", peer_addr);

    // Create a buffered reader for efficient line reading
    let mut reader = BufReader::new(&mut stream);
    let mut line = String::new();

    loop {
        line.clear(); // Clear the string for the next message
        match reader.read_line(&mut line) {
            Ok(0) => { // Client disconnected (read_line returns 0 bytes)
                println!("Rust Server: Client {} disconnected.", peer_addr);
                break;
            }
            Ok(bytes_read) => {
                let trimmed_message = line.trim(); // Remove newline and extra whitespace

                println!("Rust Server received: '{}' ({} bytes)", trimmed_message, bytes_read);

                // Check for "QUIT" message to gracefully close
                if trimmed_message.eq_ignore_ascii_case("QUIT") {
                    println!("Rust Server: Received 'QUIT'. Closing connection.");
                    let goodbye_msg = "Goodbye from Rust!";
                    stream.write_all(goodbye_msg.as_bytes())?;
                    stream.write_all(b"\n")?; // Always send a newline
                    break;
                }

                // Echo the message back to the client
                let response = format!("Rust Server Echo: {}", trimmed_message);
                stream.write_all(response.as_bytes())?;
                stream.write_all(b"\n")?; // Always send a newline for line-based reading

                // Small delay to prevent very fast loops in simple tests
                thread::sleep(Duration::from_millis(5));
            }
            Err(e) => {
                eprintln!("Rust Server: Error reading from client {}: {}", peer_addr, e);
                break;
            }
        }
    }

    println!("Rust Server: Handler for {} finished.", peer_addr);
    Ok(())
}

fn main() -> io::Result<()> {
    let address = "127.0.0.1:8080"; // The address and port for our server
    let listener = TcpListener::bind(address)?; // Start listening for connections
    println!("Rust Server: Listening on {}", address);
    println!("Rust Server: Waiting for Python client to connect...");

    // Loop to accept and handle new connections
    // For this simple example, it will handle one client and then stop if that client disconnects
    // or sends 'QUIT'. For a game, you might want to keep it running for multiple clients or
    // restart on client disconnect.
    if let Some(stream) = listener.incoming().next() { // Only accept one connection for simplicity
        match stream {
            Ok(stream) => {
                // Handle the client. In a real game, you might want to use
                // thread::spawn(move || { ... }) here to handle multiple clients concurrently.
                if let Err(e) = handle_client(stream) {
                    eprintln!("Rust Server: Error handling client: {}", e);
                }
            }
            Err(e) => {
                eprintln!("Rust Server: Error accepting connection: {}", e);
            }
        }
    } else {
        println!("Rust Server: No incoming connections.");
    }

    println!("Rust Server: Server shutting down.");
    Ok(())
}