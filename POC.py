import numpy as np
import scipy
import scipy.fftpack


class POC:

    def __init__(self, imgBlockCur, imgBlockRef, blockSize):
        self.imgBlockCur = imgBlockCur
        self.imgBlockRef = imgBlockRef
        self.blockSize = blockSize

    def hannCalc(self):
        window = np.hanning(self.blockSize)
        window = np.dot(window.T, window)

        return window

    def calcPOC(self, block_ref,block_curr ,window, mb_x, mb_y):
        # mengitung nilai setiap blok dengan fft 2 dimensi
        fft_ref = scipy.fftpack.fft2(np.dot(block_ref, window), (mb_x, mb_y)).real
        fft_curr = scipy.fftpack.fft2(np.dot(block_curr, window), (mb_x, mb_y)).real

        R1 = fft_curr * np.conj(fft_ref)
        R2 = np.abs(R1)
        R2[R2 == 0] = 1e-31
        R = np.int16(R1 / R2)
        R = scipy.fftpack.ifftn(R).real
        R = np.float_(np.round(R, 10))
        r = scipy.fftpack.fftshift(abs(R)).real

        return r


    def getPOC(self):
        mb_x = self.blockSize  # panjang macroblock
        mb_y = self.blockSize  # lebar macroblock

        # Perhitunggan Hanning Window
        window = self.hannCalc()

        img0 = self.imgBlockCur
        img1 = self.imgBlockRef

        # konversi image float ke int
        cols, rows = img0.shape
        img0 = img0.astype(int)
        img1 = img1.astype(int)

        # menghitung berapa blok yang dihasilkan
        # dengan pembagian width atau height dan dibagi dengan blocksize
        colsY = np.int16(np.floor(cols / mb_y))
        rowsX = np.int16(np.floor(rows / mb_x))

        # inisiasi untuk menyimpan matrik image yang dipecah dalam blok
        BlocksCurr = np.empty((colsY, rowsX), dtype=object)
        BlocksRef = np.empty((colsY, rowsX), dtype=object)

        # untuk mengetahui sisa pixel
        modY = cols % mb_y
        modX = rows % mb_x

        # inisiasi untuk menyimpan nilai poc
        poc = np.zeros((mb_y, mb_x, colsY * rowsX))
        coorAwal = np.zeros((colsY * rowsX,2))
        rect = np.zeros((colsY * rowsX,4))

        nm = 0
        nY = 0

        # perulangan y dan x dimulai dari 1
        # perulangan ini akan loncat sesuai dengan blocksize yang ditentukan
        # fungsi cols-modY atau rows-modX untuk pembatas, supaya area perulangan tidak melampaui ukuran gambar
        for y in range(1, cols - modY, mb_y):
            nX = 0
            for x in range(1, rows - modX, mb_x):
                # karena perulangan x dan y dimulai 1, sedangkan array image di mulai 0,
                # maka perlu dikurangi 1
                m_y = y - 1
                m_x = x - 1

                # untuk menyimpan block array yang di crop sesuai ukuran
                BlocksCurr[nY, nX] = img0[m_y:m_y + mb_y, m_x: m_x + mb_x]
                BlocksRef[nY, nX] = img1[m_y:m_y + mb_y, m_x: m_x + mb_x]

                rect[nm, :] = [m_x, m_y, mb_x, mb_y] #untuk membentuk kotak setiap blok

                block_ref = BlocksRef[nY, nX]
                block_curr = BlocksCurr[nY, nX]

                # Perhitungan POC 
                r = self.calcPOC(block_ref, block_curr, window, mb_x, mb_y)
                
                # menyimpan nilai poc sesuai nomor blok
                poc[:, :, nm] = r

                coorAwal[nm, 0] = ((nX + 1) * mb_x) - 1  # koordinat X mulai
                coorAwal[nm, 1] = ((nY + 1) * mb_y) - 1  # koordinat Y mulai

                nX += 1
                nm += 1
            nY += 1

        # kembalian nilai
        # poc : untuk penyimpanan nilai poc disetiap blok
        # coorAwal : sebagai koordinat awal penanda batas blok
        # rect : untuk menyimpak penanda kotak x y width height
        return [poc, coorAwal, rect]
