use std::io::{Read, Write};
use std::net::{TcpListener, TcpStream};

fn main() -> std::io::Result<()> {
    let listener = TcpListener::bind("127.0.0.1:5000")?;
    println!("[Rust] Listening on 127.0.0.1:5000");

    for stream in listener.incoming() {
        match stream {
            Ok(mut stream) => {
                println!("[Rust] Client connected: {:?}", stream.peer_addr());

                let mut buffer = [0; 1024];
                let size = stream.read(&mut buffer)?;
                let message = String::from_utf8_lossy(&buffer[..size]);
                println!("[Rust] Received: {}", message);

                let response = format!("Rust got: {}", message);
                stream.write_all(response.as_bytes())?;
            }
            Err(e) => {
                eprintln!("[Rust] Connection failed: {}", e);
            }
        }
    }

    Ok(())
}
