from tkinter import *
from tkinter.scrolledtext import ScrolledText

sBlocks = [
    [9, 6, 3, 2, 8, 11, 1, 7, 10, 4, 14, 15, 12, 0, 13, 5],
    [3, 7, 14, 9, 8, 10, 15, 0, 5, 2, 6, 12, 11, 4, 13, 1],
    [14, 4, 6, 2, 11, 3, 13, 8, 12, 15, 5, 10, 0, 7, 1, 9],
    [14, 7, 10, 12, 13, 1, 3, 9, 0, 2, 11, 4, 15, 8, 5, 6],
    [11, 5, 1, 9, 8, 13, 15, 0, 14, 4, 2, 3, 12, 7, 10, 6],
    [3, 10, 13, 12, 1, 2, 0, 11, 7, 5, 9, 4, 8, 14, 15, 6],
    [1, 13, 2, 9, 7, 10, 6, 0, 8, 12, 4, 5, 15, 3, 11, 14],
    [11, 10, 15, 5, 0, 12, 14, 8, 6, 2, 3, 9, 1, 7, 13, 4]
]

class InterfaceApp:

    def __init__(self, root):
        self.root = root
        self.root['bg'] = '#cddafa'
        self.root.title('Гост 28147-89')
        self.root.geometry('1100x600')

        frame = Frame(root, bg='white')
        frame.place(relx=0.05, rely=0.08, width=1000, height=500)

        labelInpt = Label(frame, text='Введите текст:', bg='#cddafa', font=10, anchor="nw")
        labelInpt.grid(row=0, column=0, padx=80, pady=5, sticky='w')

        self.textInpt = ScrolledText(frame, width=100, height=8, relief="solid")
        self.textInpt.grid(row=1, column=0, padx=80, pady=5, sticky='w')

        labelKey = Label(frame, text='Введите ключ:', bg='#cddafa', font=10, anchor="nw")
        labelKey.grid(row=4, column=0, padx=80, pady=5, sticky='w')

        self.key = Entry(frame, width=133, borderwidth=1, relief="solid")
        self.key.grid(row=6, column=0, padx=80, pady=5, sticky="w")

        labelOutpt = Label(frame, text='Результат:', bg='#cddafa', font=10, anchor="nw")
        labelOutpt.grid(row=7, column=0, padx=80, pady=5, sticky='w')

        self.textOutpt = ScrolledText(frame, width=100, height=8, relief="solid")
        self.textOutpt.grid(row=8, column=0, padx=80, pady=5, sticky='w')
        self.textOutpt.config(state=DISABLED)

        btnEncrypt = Button(frame, text='Зашифровать', bg='#cddafa', command=self.btnClick)
        btnEncrypt.grid(row=10, column=0, sticky="w", padx=80, pady=10)

    def btnClick(self):

        sourceText = self.textInpt.get("1.0", END).strip()
        keyHex = self.key.get().strip()

        if not sourceText:
            self.textOutpt.config(state=NORMAL)
            self.textOutpt.delete("1.0", END)
            self.textOutpt.insert(END, "Ошибка: текст не может быть пустым")
            self.textOutpt.config(state=DISABLED)
            return

        try:
            if len(keyHex) != 64:
                raise ValueError("Ключ должен содержать 64 символа в шестнадцатеричном формате.")
            key = int(keyHex, 16)
            encryptedText = self.gostEncrypt(sourceText, key)
            self.textOutpt.config(state=NORMAL)
            self.textOutpt.delete("1.0", END)
            self.textOutpt.insert(END, encryptedText)
            self.textOutpt.config(state=DISABLED)
        except Exception as e:
            self.textOutpt.config(state=NORMAL)
            self.textOutpt.delete("1.0", END)
            self.textOutpt.insert(END, f"Ошибка: {str(e)}")
            self.textOutpt.config(state=DISABLED)

    def gostEncrypt(self, text, key):

        textBin=''
        for char in text:
            textBin += format(ord(char), '08b')
        textBin = textBin.ljust((len(textBin) + 63) // 64 * 64, '0')

        # Дополняем текст нулями, если его длина не кратна 64
        while len(textBin) % 64 != 0:
            textBin += '0'

        for i in range(0, len(textBin), 64):
            blocks = [textBin[i:i + 64]]

        keys = [0] * 8
        for i in range(8):
            keys[i] = (key >> (32 * i)) & 0xFFFFFFFF

        encryptedBlocks = []
        for block in blocks:
            left = int(block[:32], 2)
            right = int(block[32:], 2)

            for i in range(32):
                roundKey = keys[i % 8]
                temp = (right + i + roundKey) % (1 << 32)
                sOutput = self.sBoxSubstitution(temp)
                left, right = right, (left ^ sOutput) % (1 << 32)

            left, right = right, left

            encryptedBlocks.append(format((left << 32) | right, '064b'))

        encryptedText = ''.join(encryptedBlocks)
        return hex(int(encryptedText, 2))[2:]

    def sBoxSubstitution(self, value):

        output = 0
        for i in range(8):
            nibble = (value >> (4 * i)) & 0b1111
            output |= (sBlocks[i][nibble] << (4 * i))
        return output

if __name__ == '__main__':

    root = Tk()
    app = InterfaceApp(root)
    root.mainloop()
