# -*- coding: utf-8 -*-
"""dcgan.ipynb

Automatically generated by Colaboratory.
Twórcy:
Paweł Szyszkowski s18184, Braian Kreft s16723, Maciej Dzieciuch s16737
Original file is located at
    https://colab.research.google.com/drive/15ORUPiveJ2U8VZ9CqvYRDeMtYozVbwuw
"""

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline

from google.colab import drive
drive.mount('/content/drive')

"""Generative Adversarial Networks
-------------------------------

Co to jest GAN?
-------------------------------
GAN-y są ramą do uczenia modelu DL, aby uchwycić rozkład danych treningowych, aby móc generować nowe dane z tej samej dystrybucji. GANy zostały wynalezione przez Iana Goodfellow w 2014 roku i po raz pierwszy opisane w pracy `Generative Adversarial`. Składają się one z dwóch odrębnych modeli, *generator* i *discriminator*. Zadaniem generatora jest tworzenie 'fałszywych' obrazów, które wyglądają jak obrazy szkoleniowe. Zadaniem dyskryminatora jest spojrzenie na obraz i określenie, czy jest to prawdziwy obraz treningowy, czy też fałszywy obraz z generatora. Podczas treningu, generator nieustannie próbuje przechytrzyć dyskryminatora, generując coraz lepsze podróbki, podczas gdy dyskryminator pracuje, aby stać się lepszym detektywem i poprawnie klasyfikować prawdziwe i fałszywe obrazy. Równowaga w tej grze jest wtedy, gdy generator generuje doskonałe
podróbki, które wyglądają tak, jakby pochodziły bezpośrednio z danych treningowych, a dyskryminator zawsze zgaduje z 50% pewnością, że wyjście generatora jest prawdziwe lub fałszywe.



Co to jest DCGAN?
-------------------------------

DCGAN jest bezpośrednim rozszerzeniem GAN opisanego powyżej, z tą różnicą, że jawnie wykorzystuje warstwy konwolucyjne i konwolucyjno-transpozycyjne w dyskryminatorze i generatorze. Po raz pierwszy został on opisany przez Radford w pracy `Unsupervised Representation Learning With
Deep Convolutional Generative Adversarial Networks`.  Dane wejściowe to obraz wejściowy 3x64x64, a dane wyjściowe to
skalarne prawdopodobieństwo, że dane wejściowe pochodzą z rozkładu danych rzeczywistych. Warstwy conv-transpose pozwalają na przekształcenie wektora ukrytego w wolumen o takim samym kształcie jak obraz. W artykule autorzy podają również wskazówki, jak skonfigurować optymalizatory, jak obliczyć funkcje straty, oraz jak zainicjować wagi modelu.


"""

from __future__ import print_function
#%matplotlib inline
import argparse
import os
import random
import torch
import torch.nn as nn
import torch.nn.parallel
import torch.backends.cudnn as cudnn
import torch.optim as optim
import torch.utils.data
import torchvision.datasets as dset
import torchvision.transforms as transforms
import torchvision.utils as vutils
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython.display import HTML

# Set random seed for reproducibility
manualSeed = 999
#manualSeed = random.randint(1, 10000) # use if you want new results
print("Random Seed: ", manualSeed)
random.seed(manualSeed)
torch.manual_seed(manualSeed)

"""Dane wejściowe
------

Zdefiniujmy kilka danych wejściowych dla przebiegu:

- **dataroot** - ścieżka do katalogu głównego zbioru danych. Więcej  na temat zbioru danych w następnym rozdziale
- **workers** - liczba wątków robotniczych ładujących dane za pomocą  DataLoader
- **batch_size** - wielkość partii używanej podczas treningu. W dokumencie DCGAN używa partii o wielkości 128
- **image_size** - przestrzenny rozmiar obrazów używanych do treningu. W tej implementacji domyślnie ustawiony jest rozmiar 64x64. Jeśli pożądany jest inny rozmiar,  należy zmienić struktury D i G.
- **nc** - liczba kanałów kolorystycznych w obrazach wejściowych. Dla obrazów kolorowych
   jest to 3
- **nz** - długość wektora ukrytego
- **ngf** - odnosi się do głębokości map cech przenoszonych przez generator
- **ndf** - określa głębokość map cech propagowanych przez  dyskryminator
- **num_epochs** - liczba epok treningowych do wykonania. Dłuższy trening prawdopodobnie przyniesie lepsze rezultaty, ale będzie też trwał znacznie dłużej
- **lr** - współczynnik uczenia dla treningu. Jak opisano w dokumencie DCGAN,  liczba ta powinna wynosić 0,0002
- **beta1** - hiperparametr beta1 dla optymalizatorów Adama. Zgodnie z opisem w dokumencie, liczba ta powinna wynosić 0,5
- **ngpu** - liczba dostępnych procesorów graficznych. Jeśli wartość ta wynosi 0, kod będzie działał w trybie
   trybie CPU. Jeśli liczba ta jest większa od 0, kod będzie działał na tej liczbie  procesorów graficznych



"""

# Root directory for dataset
dataroot = "drive/MyDrive/Colab Notebooks/images2/landscape/"

# Number of workers for dataloader
workers = 2

# Batch size during training
batch_size = 32

# Spatial size of training images. All images will be resized to this
#   size using a transformer.
image_size = 64

# Number of channels in the training images. For color images this is 3
nc = 3

# Size of z latent vector (i.e. size of generator input)
nz = 100

# Size of feature maps in generator
ngf = 64

# Size of feature maps in discriminator
ndf = 64

# Number of training epochs
num_epochs = 160

# Learning rate for optimizers
lr = 0.0002

# Beta1 hyperparam for Adam optimizers
beta1 = 0.5

# Number of GPUs available. Use 0 for CPU mode.
ngpu = 1

"""Zestaw danych
----

W tym algorytmie użyjemy zbioru danych pobranych ze strony wikiart.org za pomocą scrappera. 



"""

# Create the dataset
dataset = dset.ImageFolder(root=dataroot,
                           transform=transforms.Compose([
                               transforms.Resize(image_size),
                               transforms.CenterCrop(image_size),
                               transforms.ToTensor(),
                               transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
                           ]))
# Create the dataloader
dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size,
                                         shuffle=True, num_workers=workers)

# Decide which device we want to run on
device = torch.device("cuda:0" if (torch.cuda.is_available() and ngpu > 0) else "cpu")

# Plot some training images
real_batch = next(iter(dataloader))
plt.figure(figsize=(8,8))
plt.axis("off")
plt.title("Training Images")
plt.imshow(np.transpose(vutils.make_grid(real_batch[0].to(device)[:64], padding=2, normalize=True).cpu(),(1,2,0)))

"""Implementacja
--------------

Mając ustawione parametry wejściowe i przygotowany zbiór danych, możemy teraz przejść do implementacji. Zaczniemy od strategii inicjalizacji wagi, następnie omówimy szczegółowo generator, dyskryminator, funkcje straty oraz pętlę treningową.

Inicjalizacja wagi
--------------

W dokumencie DCGAN autorzy podają, że wszystkie wagi modelu powinny być losowo inicjalizowane z rozkładu normalnego o wartościach mean=0, stdev=0.02. Funkcja weights_init przyjmuje na wejściu zainicjalizowany model i ponownie inicjalizuje wszystkie warstwy konwolucyjne, konwolucyjno-transpozycyjne oraz warstwy normalizacji wsadowej, aby spełniały te kryteria. Funkcja ta jest stosowana do modeli natychmiast po inicjalizacji.



"""

# custom weights initialization called on netG and netD
def weights_init(m):
    classname = m.__class__.__name__
    if classname.find('Conv') != -1:
        nn.init.normal_(m.weight.data, 0.0, 0.02)
    elif classname.find('BatchNorm') != -1:
        nn.init.normal_(m.weight.data, 1.0, 0.02)
        nn.init.constant_(m.bias.data, 0)

"""**Generator**
------

Generator $G$, jest przeznaczony do odwzorowania wektora przestrzeni ukrytej ($z$) do przestrzeni danych. Ponieważ nasze dane są obrazami, konwersja $z$ do przestrzeni danych oznacza ostatecznie utworzenie obrazu RGB o tym samym rozmiarze, co obrazy treningowe (tj. 3x64x64). W praktyce, jest to osiągane poprzez serię dwuwymiarowych warstw konwolucyjnych
warstw transpozycji, z których każda jest sparowana z warstwą 2d batch norm i warstwą relu. Wyjście generatora jest przepuszczane przez funkcję tanh aby zwrócić je do zakresu danych wejściowych $[-1,1]$. Warto zwrócić uwagę na istnienie funkcji batch norm po 
warstwach conv-transpose, gdyż jest to kluczowy wkład pracy DCGAN. Warstwy te pomagają w przepływie gradientów podczas treningu. 
Zauważ, jak dane wejściowe, które ustawiliśmy w sekcji wejściowej (*nz*, *ngf* i*nc*) wpływają na architekturę generatora w kodzie. *nz* to długość wektora wejściowego z, *ngf* odnosi się do rozmiaru map cech które są propagowane przez generator, a *nc* jest liczbą kanałów w obrazie wyjściowym (ustawiona na 3 dla obrazów RGB). 
Poniżej znajduje się kod generatora.



"""

# Generator Code

class Generator(nn.Module):
    def __init__(self, ngpu):
        super(Generator, self).__init__()
        self.ngpu = ngpu
        self.main = nn.Sequential(
            # input is Z, going into a convolution
            nn.ConvTranspose2d( nz, ngf * 8, 4, 1, 0, bias=False),
            nn.BatchNorm2d(ngf * 8),
            nn.ReLU(True),
            # state size. (ngf*8) x 4 x 4
            nn.ConvTranspose2d(ngf * 8, ngf * 4, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf * 4),
            nn.ReLU(True),
            # state size. (ngf*4) x 8 x 8
            nn.ConvTranspose2d( ngf * 4, ngf * 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf * 2),
            nn.ReLU(True),
            # state size. (ngf*2) x 16 x 16
            nn.ConvTranspose2d( ngf * 2, ngf, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf),
            nn.ReLU(True),
            # state size. (ngf) x 32 x 32
            nn.ConvTranspose2d( ngf, nc, 4, 2, 1, bias=False),
            nn.Tanh()
            # state size. (nc) x 64 x 64
        )

    def forward(self, input):
        return self.main(input)

"""Teraz możemy zainicjować generator i zastosować funkcję ``weights_init``. Sprawdź wyświetlony model, aby zobaczyć jak obiekt generatora jest
zbudowany.
"""

# Create the generator
netG = Generator(ngpu).to(device)

# Handle multi-gpu if desired
if (device.type == 'cuda') and (ngpu > 1):
    netG = nn.DataParallel(netG, list(range(ngpu)))

# Apply the weights_init function to randomly initialize all weights
#  to mean=0, stdev=0.2.
netG.apply(weights_init)

# Print the model
print(netG)

"""Dyskryminator
----------

Jak wspomniano, dyskryminator $D$, jest binarną siecią klasyfikacji, która przyjmuje obraz jako dane wejściowe i wypisuje skalarne prawdopodobieństwo, że obraz wejściowy jest prawdziwy. Tutaj $D$ bierze obraz wejściowy 3x64x64, przetwarza go przez serię Conv2d, BatchNorm2d, i warstwy LeakyReLU, i wypisuje końcowe prawdopodobieństwo poprzez sigmoidalną funkcję aktywacji. Architektura ta może być rozszerzona
o więcej warstw, jeśli jest to konieczne dla danego problemu.  Funkcje batch norm i leaky relu promują zdrowy przepływ gradientu, który jest krytyczny dla procesu uczenia się zarówno $G$ jak i $D$.



"""

class Discriminator(nn.Module):
    def __init__(self, ngpu):
        super(Discriminator, self).__init__()
        self.ngpu = ngpu
        self.main = nn.Sequential(
            # input is (nc) x 64 x 64
            nn.Conv2d(nc, ndf, 4, 2, 1, bias=False),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (ndf) x 32 x 32
            nn.Conv2d(ndf, ndf * 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ndf * 2),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (ndf*2) x 16 x 16
            nn.Conv2d(ndf * 2, ndf * 4, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ndf * 4),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (ndf*4) x 8 x 8
            nn.Conv2d(ndf * 4, ndf * 8, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ndf * 8),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (ndf*8) x 4 x 4
            nn.Conv2d(ndf * 8, 1, 4, 1, 0, bias=False),
            nn.Sigmoid()
        )

    def forward(self, input):
        return self.main(input)

"""Teraz, tak jak w przypadku generatora, możemy utworzyć dyskryminator, zastosować funkcję
funkcję ``weights_init`` i wydrukować strukturę modelu.


"""

# Create the Discriminator
netD = Discriminator(ngpu).to(device)

# Handle multi-gpu if desired
if (device.type == 'cuda') and (ngpu > 1):
    netD = nn.DataParallel(netD, list(range(ngpu)))
    
# Apply the weights_init function to randomly initialize all weights
#  to mean=0, stdev=0.2.
netD.apply(weights_init)

# Print the model
print(netD)

"""Funkcje strat i optymalizatory
-------

Mając ustawione $D$ i $G$, możemy określić jak się uczą
poprzez funkcje straty i optymalizatory. Użyjemy binarnego krzyża
który jest zdefiniowana w PyTorch jako:

\begin{align}\ell(x, y) = L = \{l_1,\dots,l_N\}^\top, \quad l_n = - \left[ y_n \cdot \log x_n + (1 - y_n) \cdot \log (1 - x_n) \right]\end{align}

Zauważmy, że funkcja ta umożliwia obliczenie obu składników logarytmicznych w funkcji celu (tzn. $log(D(x))$ i $log(1-D(G(x))$).
$log(1-D(G(z)))$). Możemy określić, która część równania BCE ma być użyta w przypadku danych wejściowych $y$. Dokonujemy tego w pętli treningowej, która pojawi się za chwilę, ale ważne jest, aby zrozumieć, w jaki sposób możemy wybrać, który składnik chcemy obliczyć, zmieniając tylko wartość $y$.
(tj. etykiety GT).

Następnie definiujemy naszą prawdziwą etykietę jako 1, a fałszywą jako 0, etykiety będą używane podczas obliczania strat $D$ i $G$. Na koniec ustawiamy dwa osobne optymalizatory, jeden dla $D$ i jeden dla $G$. Jak podano w pracy DCGAN, oba są optymalizatorami Adam o współczynniku uczenia 0,0002 i Beta1 = 0,5. Aby śledzić postępy w uczeniu się generatora, będziemy generować stałą partię wektorów ukrytych, które są losowane z rozkładu gaussowskiego (tj. fixed_noise) . W pętli treningowej będziemy okresowo wprowadzać ten stały szum do $G$, i przez iteracje będziemy widzieć obrazy formujące się z szumu.



"""

# Initialize BCELoss function
criterion = nn.BCELoss()

# Create batch of latent vectors that we will use to visualize
#  the progression of the generator
fixed_noise = torch.randn(64, nz, 1, 1, device=device)

# Establish convention for real and fake labels during training
real_label = 1.
fake_label = 0.

# Setup Adam optimizers for both G and D
optimizerD = optim.Adam(netD.parameters(), lr=lr, betas=(beta1, 0.999))
optimizerG = optim.Adam(netG.parameters(), lr=lr, betas=(beta1, 0.999))

"""Szkolenia
-------------------------------

Wreszcie, teraz, gdy mamy już zdefiniowane wszystkie części ramy GAN, możemy go trenować. Należy pamiętać, że trenowanie GAN jest w pewnym sensie formą sztuki, ponieważ nieprawidłowe ustawienia hiperparametrów prowadzą do załamania trybu z
z niewielkim wyjaśnieniem, co poszło nie tak. Tutaj będziemy ściśle naśladować Algorytm 1 z pracy Goodfellow'a, jednocześnie przestrzegając niektórych z najlepszych praktyk
praktyk pokazanych w `ganhacks`.
Mianowicie, "skonstruujemy różne mini-partie dla prawdziwych i fałszywych obrazów",  a także dostosujemy funkcję celu G, aby zmaksymalizować $logD(G(z))$. Trening podzielony jest na dwie główne części. 
Część 1 uaktualnia Dyskryminator, a część 2 uaktualnia Generator.

**Część 1 - Trening Dyskryminatora**

Przypomnijmy, że celem treningu dyskryminatora jest zmaksymalizowanie prawdopodobieństwa poprawnej klasyfikacji danych wejściowych jako prawdziwe lub fałszywe. W
Goodfellow'a, chcemy "aktualizować dyskryminator poprzez wzrastający jego gradientu stochastycznego". Praktycznie, chcemy zmaksymalizować $log(D(x)) + log(1-D(G(z)))$. Ze względu na oddzielną mini-batch sugestię od ganhacks, obliczymy to w dwóch krokach. Po pierwsze, skonstruujemy partię rzeczywistych próbek z zestawu treningowego, przejdziemy przez $D$, obliczymy stratę ($log(D(x))$), a następnie obliczymy gradienty w przejściu wstecz. Po drugie, skonstruujemy partię fałszywych próbek za pomocą bieżącego generatora, przepuścimy tę partię
przez $D$, obliczymy stratę ($log(1-D(G(z)))$), i *akumulujemy* gradienty za pomocą przejścia wstecznego. Teraz, mając
gradienty z obu partii, zarówno prawdziwych, jak i fałszywych, wywołujemy krok optymalizatora Dyskryminatora.

**Część 2 - Trening Generatora**

Jak napisano w oryginalnym artykule, chcemy wytrenować Generator poprzez minimalizację $log(1-D(G(z)))$ w celu wygenerowania lepszych fałszywek. Jak wspomniano, Goodfellow wykazał, że nie zapewnia to wystarczających gradientów, szczególnie na wczesnym etapie procesu uczenia. Jako poprawkę, chcemy zamiast tego maksymalizować $log(D(G(z)))$. W kodzie osiągamy to poprzez: sklasyfikowanie wyjścia generatora z części 1 za pomocą Dyskryminatora, obliczamy straty G *używając prawdziwych etykiet jako GT*, obliczamy gradienty G w przejściu wstecznym, i w końcu uaktualnieniamy parametry G
za pomocą kroku optymalizatora. Może się wydawać, że użycie prawdziwych etykiet jako etykiet GT dla funkcji straty, ale to pozwala nam na użycie części $log(x)$ BCELoss (zamiast $log(1-x)$), co jest dokładnie tym, czego chcemy.

Na koniec zajmiemy się raportowaniem statystyk na koniec każdej epoki, przepuścimy przez generator naszą partię fixed_noise, aby
wizualnie śledzić postępy w treningu G. Statystyki treningu
raportowane są następujące:

- **Loss_D** - strata dyskryminatora obliczona jako suma strat dla
   wszystkich prawdziwych i wszystkich fałszywych partii ($log(D(x)) + log(D(G(z)))$).
- **Loss_G** - strata generatora obliczona jako $log(D(G(z)))$.
- **D(x)** - średnia wartość wyjściowa (w całej partii) dyskryminatora  dla całej rzeczywistej partii. Powinna ona zaczynać się od wartości zbliżonej do 1, a następnie  teoretycznie zbiegać się do 0.5, gdy G staje się lepsze.
- **D(G(z))** - średnie wyniki dyskryminatora dla całej fałszywej partii.  Pierwsza liczba jest przed uaktualnieniem D, a druga liczba jest  po uaktualnieniu D. Liczby te powinny zaczynać się w pobliżu 0 i zbiegać się do  0.5 w miarę jak G staje się coraz lepsze. 
"""

# Commented out IPython magic to ensure Python compatibility.
# Training Loop

# Lists to keep track of progress
img_list = []
G_losses = []
D_losses = []
iters = 0

print("Starting Training Loop...")
# For each epoch
for epoch in range(num_epochs):
    # For each batch in the dataloader
    for i, data in enumerate(dataloader, 0):
        
        ############################
        # (1) Update D network: maximize log(D(x)) + log(1 - D(G(z)))
        ###########################
        ## Train with all-real batch
        netD.zero_grad()
        # Format batch
        real_cpu = data[0].to(device)
        b_size = real_cpu.size(0)
        label = torch.full((b_size,), real_label, dtype=torch.float, device=device)
        # Forward pass real batch through D
        output = netD(real_cpu).view(-1)
        # Calculate loss on all-real batch
        errD_real = criterion(output, label)
        # Calculate gradients for D in backward pass
        errD_real.backward()
        D_x = output.mean().item()

        ## Train with all-fake batch
        # Generate batch of latent vectors
        noise = torch.randn(b_size, nz, 1, 1, device=device)
        # Generate fake image batch with G
        fake = netG(noise)
        label.fill_(fake_label)
        # Classify all fake batch with D
        output = netD(fake.detach()).view(-1)
        # Calculate D's loss on the all-fake batch
        errD_fake = criterion(output, label)
        # Calculate the gradients for this batch
        errD_fake.backward()
        D_G_z1 = output.mean().item()
        # Add the gradients from the all-real and all-fake batches
        errD = errD_real + errD_fake
        # Update D
        optimizerD.step()

        ############################
        # (2) Update G network: maximize log(D(G(z)))
        ###########################
        netG.zero_grad()
        label.fill_(real_label)  # fake labels are real for generator cost
        # Since we just updated D, perform another forward pass of all-fake batch through D
        output = netD(fake).view(-1)
        # Calculate G's loss based on this output
        errG = criterion(output, label)
        # Calculate gradients for G
        errG.backward()
        D_G_z2 = output.mean().item()
        # Update G
        optimizerG.step()
        
        # Output training stats
        if i % 150 == 0:
            print('[%d/%d][%d/%d]\tLoss_D: %.4f\tLoss_G: %.4f\tD(x): %.4f\tD(G(z)): %.4f / %.4f'
#                   % (epoch, num_epochs, i, len(dataloader),
                     errD.item(), errG.item(), D_x, D_G_z1, D_G_z2))
        
        # Save Losses for plotting later
        G_losses.append(errG.item())
        D_losses.append(errD.item())
        
        # Check how the generator is doing by saving G's output on fixed_noise
        if (iters % 2100 == 0) or ((epoch == num_epochs-1) and (i == len(dataloader)-1)):
            with torch.no_grad():
                fake = netG(fixed_noise).detach().cpu()
            img_list.append(vutils.make_grid(fake, padding=2, normalize=True))
            
        iters += 1

"""Wyniki
-------

Na koniec sprawdźmy, jak nam poszło. Przyjrzymy się tutaj trzem
różnym wynikom. Po pierwsze, zobaczymy jak zmieniały się straty D i G podczas treningu. Po drugie, zwizualizujemy wynik G na fixed_noise dla każdej epoki. I po trzecie, spojrzymy na partię prawdziwych danych obok partii fałszywych danych z G.

**Strata w zależności od iteracji treningowej**

Poniżej znajduje się wykres strat D i G w zależności od iteracji treningowych.
"""

plt.figure(figsize=(10,5))
plt.title("Generator and Discriminator Loss During Training")
plt.plot(G_losses,label="G")
plt.plot(D_losses,label="D")
plt.xlabel("iterations")
plt.ylabel("Loss")
plt.legend()
plt.show()

"""**Wizualizacja progresji G**

Zapisywaliśmy wyjście generatora na wsad fixed_noise po każdym treningu. Teraz możemy zwizualizować G za pomocą animacji. 
"""

#%%capture
fig = plt.figure(figsize=(8,8))
plt.axis("off")
ims = [[plt.imshow(np.transpose(i,(1,2,0)), animated=True)] for i in img_list]
ani = animation.ArtistAnimation(fig, ims, interval=1000, repeat_delay=1000, blit=True)

HTML(ani.to_jshtml())

"""**Prawdziwe obrazy vs. Fałszywe obrazy**

Na koniec, spójrzmy na kilka prawdziwych i fałszywych obrazów obok siebie.

"""

# Grab a batch of real images from the dataloader
real_batch = next(iter(dataloader))

# Plot the real images
plt.figure(figsize=(15,15))
plt.subplot(1,2,1)
plt.axis("off")
plt.title("Real Images")
plt.imshow(np.transpose(vutils.make_grid(real_batch[0].to(device)[:64], padding=5, normalize=True).cpu(),(1,2,0)))

# Plot the fake images from the last epoch
plt.subplot(1,2,2)
plt.axis("off")
plt.title("Fake Images")
plt.imshow(np.transpose(img_list[-1],(1,2,0)))
plt.show()
