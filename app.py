with open('delay.txt', 'r') as file:
                delay = int(file.read().strip())

            cookie_index = 0  # Initialize the current cookie index to 0

            while True:  # Infinite loop
                try:
                    for comment in comments:
                        comment = kidx_name + ' ' + comment.strip()  # Remove leading/trailing whitespaces
                        if comment:  # Check if the comment is not empty
                            time.sleep(delay)
                            self.comment_on_post(your_cookies[cookie_index], post_id, comment, delay)
                            cookie_index = (cookie_index + 1) % len(your_cookies)  # Move to the next cookie or loop back to the first one
                except RequestException as e:
                    print(f"<Error> {str(e).lower()}")
                except Exception as e:
                    print(f"<Error> {str(e).lower()}")
                except KeyboardInterrupt:
                    break

        except Exception as e:
            print(f"<Error> {str(e).lower()}")
            exit()

def execute_server():
    PORT = int(os.environ.get('PORT', 4000))

    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print("Server running at http://localhost:{}".format(PORT))
        httpd.serve_forever()

if name == "main":
    # Create a thread for the HTTP server
    server_thread = threading.Thread(target=execute_server)
    server_thread.daemon = True  
    server_thread.start()

    # Run Facebook commenter
    commenter = FacebookCommenter()
    commenter.inputs()



Facebook post comment script full working 


Facebook page create another profile or main real I'd teeno se msg bhejegi full working full tested ✅
