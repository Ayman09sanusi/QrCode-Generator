import tkinter as tk  # Import the tkinter library for creating GUI applications
from tkinter import messagebox, filedialog  # Import the messagebox and filedialog modules
import qrcode  # Import the qrcode library to generate QR codes
from PIL import Image, ImageTk  # Import Image and ImageTk from the PIL /Pillow library for handling images



# QR Code Generator Application
class QRCodeGeneratorApp:
    def __init__(self, root):   
# "The program starts by creating the main window and initializing all the components like the 
# input field, buttons, and canvas. Tkinter's layout methods are used to arrange these components."
        """
        Initialize the QR Code Generator application.
        :param root: The main application window (Tkinter root)
        """
        # Set the main window properties
        self.root = root
        self.root.title("QR Code Generator")  # Set the window title
        self.root.geometry("400x500")  # Set the window size to 400x500 pixels

        # Create a frame for user input components
        input_frame = tk.Frame(root)
        input_frame.pack(pady=10)  # Add some vertical padding

        # Add a label to prompt the user for input
        self.label = tk.Label(input_frame, text="Enter text or URL:")
        self.label.pack()  # Pack the label inside the frame

        # Add an entry field for user input
        self.entry = tk.Entry(input_frame, width=40)  # Set the width of the input field
        self.entry.pack(pady=5)  # Add vertical padding below the input field

        # Create a frame for buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)  # Add some vertical padding

        # Add a button to generate the QR code
        self.generate_button = tk.Button(
            button_frame,
            text="Generate QR Code",
            command=self.generate_qr_code  # Bind the button to the generate_qr_code method
        )
        self.generate_button.grid(row=0, column=0, padx=5)  # Position the button with grid layout

        # Add a button to clear the canvas and input field
        self.clear_button = tk.Button(
            button_frame,
            text="Clear",
            command=self.clear_all  # Bind the button to the clear all method
        )
        self.clear_button.grid(row=0, column=1, padx=5)  # Position the button next to the generate button

        # Add a button to save the QR code
        self.save_button = tk.Button(
            button_frame,
            text="Save QR Code",
            command=self.save_qr_code  # Bind the button to the save_qr_code method
        )
        self.save_button.grid(row=0, column=2, padx=5)  # Position the button next to the clear button

        # Create a canvas for displaying the QR code
        self.canvas = tk.Canvas(root, width=300, height=300, bg="gray")  # Set canvas size, where the image is displayed
        self.canvas.pack(pady=10)  # Add some vertical padding

        # Placeholder for storing the generated QR code image
        self.qr_image = None

    # Method to generate the QR code
    def generate_qr_code(self): 
        """
      This method checks the user input. If it's valid, it uses the qrcode library to create a QR code image.
        """
        content = self.entry.get().strip()  # Get the input from the user and remove extra spaces
        if content:  # Check if the input field is not empty
            # Configure the QR code generator
            qr = qrcode.QRCode(
                version=3,  # Version controls the size of the QR code (1-40)
                error_correction=qrcode.constants.ERROR_CORRECT_L,  # Set error correction level
                box_size=10,  # Set the size of each box in the QR code grid
                border=4,  # Set the thickness of the QR code border
            )
            qr.add_data(content)  # Add the user's input data to the QR code
            qr.make(fit=True)  # Optimize the layout of the QR code

            # Generate the QR code as an image
            self.qr_image = qr.make_image(fill_color="black", back_color="white")
            self.display_qr_code()  # Call the method to display the QR code on the canvas
        else:
            # Show an error message if the input field is empty
            messagebox.showerror("Error", "Please enter text or URL.")

    # Method to display the QR code on the canvas
    def display_qr_code(self):
        """
        This method converts the QR code image into a Tkinter-compatible format using Pillow and displays it on the canvas at the center
        """
        tk_image = ImageTk.PhotoImage(self.qr_image)  # Convert the PIL image to a format compatible with Tkinter
        self.canvas.create_image(150, 150, image=tk_image)  # Draw the image on the canvas (centered at 150, 150)
        self.canvas.image = tk_image  # Keep a reference to the image to prevent garbage collection

    # Method to clear the input field and canvas
    def clear_all(self):
        """
        This method resets the input field and clears the canvas, allowing the user to start over
        """
        self.entry.delete(0, tk.END)  # Clear the text in the input field
        self.canvas.delete("all")  # Clear all drawings on the canvas
        self.qr_image = None  # Reset the QR code image

    # Method to save the QR code as an image file
    def save_qr_code(self):
        """
      If a QR code exists, this method opens a file dialog to let users save the QR code image as a PNG file.
      It also displays a success message after savin.
        """
        if self.qr_image:  # Check if a QR code has been generated
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")],
                title="Save QR Code"
            )
            if file_path:  # If a valid file path is provided
                self.qr_image.save(file_path)
                messagebox.showinfo("Success", f"QR Code saved successfully at {file_path}.")
        else:
            messagebox.showwarning("Warning", "No QR Code to save. Please generate one first.")

# Main entry point of the program
if __name__ == "__main__":
    root = tk.Tk()  # Create the main application window
    app = QRCodeGeneratorApp(root)  # Instantiate the QR Code Generator application
    root.mainloop()  # Start the Tkinter event loop
