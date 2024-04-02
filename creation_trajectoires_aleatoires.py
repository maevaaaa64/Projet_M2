# Fichier: creation_dataset.py

import numpy as np
import matplotlib.pyplot as plt

'''def aleaGauss(sigma):
    U1 = random.random()
    U2 = random.random()
    return sigma*math.sqrt(-2*math.log(U1))*math.cos(2*math.pi*U2)'''

def generate_sensor_trajectory_3D(T, sample_rate=200, speed_kmh=50, noise_level=0.1):
    # Convertir la vitesse en m/s
    speed_ms = speed_kmh * 1000 / 3600  # Conversion de km/h en m/s

    # Calculer la taille du pas en fonction de la vitesse et de la fréquence d'échantillonnage
    step_size = speed_ms / sample_rate

    # Initialiser les coordonnées du robot
    x = 0
    y = 0
    z = 0

    # Initialiser la liste des coordonnées de la trajectoire
    trajectory = []
    trajectory_noisy = []

    # Ajouter les coordonnées initiales à la trajectoire
    trajectory.append((x, y, z))
    trajectory_noisy.append((x, y, z))

    # Générer les déplacements aléatoires du robot
    for _ in range(T):
        # Générer des angles aléatoires pour les déplacements en x, y et z
        angle_xy = np.random.uniform(0, 2*np.pi)
        angle_z = np.random.uniform(0, np.pi)  # Limiter l'angle z à pi pour rester dans la moitié de l'espace

        # Calculer les déplacements en x, y et z
        dx = step_size * np.cos(angle_xy)
        dy = step_size * np.sin(angle_xy)
        dz = step_size * np.sin(angle_z)

        # Mettre à jour les coordonnées du robot
        x += dx
        y += dy
        z += dz

        # Ajout de bruit gaussien
        x_bruite = x + np.random.normal(scale=noise_level)
        y_bruite = y + np.random.normal(scale=noise_level)
        z_bruite = z + np.random.normal(scale=noise_level)


        # Ajouter les nouvelles coordonnées à la trajectoire
        trajectory_noisy.append((x_bruite, y_bruite, z_bruite))
        trajectory.append((x, y, z))

    return trajectory, trajectory_noisy

def plot_dual_trajectory_3D(real_trajectory, noisy_trajectory):
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(121, projection='3d')
    ay = fig.add_subplot(122, projection='3d')

    # Trajectoire réelle
    real_x_coords = [point[0] for point in real_trajectory]
    real_y_coords = [point[1] for point in real_trajectory]
    real_z_coords = [point[2] for point in real_trajectory]
    ax.plot(real_x_coords, real_y_coords, real_z_coords, marker='.', label='Trajectoire Réelle')

    # Trajectoire bruitée
    noisy_x_coords = [point[0] for point in noisy_trajectory]
    noisy_y_coords = [point[1] for point in noisy_trajectory]
    noisy_z_coords = [point[2] for point in noisy_trajectory]
    ay.plot(noisy_x_coords, noisy_y_coords, noisy_z_coords, marker='.', label='Trajectoire Bruitée')

    plt.suptitle('Trajectoires Réelle et Bruitée du parachutiste en 3D')
    ax.set_xlabel('Coordonnée x')
    ax.set_ylabel('Coordonnée y')
    ax.set_zlabel('Coordonnée z')
    ax.legend()

    ay.set_xlabel('Coordonnée x')
    ay.set_ylabel('Coordonnée y')
    ay.set_zlabel('Coordonnée z')
    ay.legend()
    plt.show()

def creation_dataset(num_samples, T, sample_rate=200, speed_kmh=50, noise_level=10):
    dataset = []
    for _ in range(num_samples):
        real_trajectory, noisy_trajectory = generate_sensor_trajectory_3D(T, sample_rate, speed_kmh, noise_level)
        dataset.append((real_trajectory, noisy_trajectory))
    return dataset

# Exemple d'utilisation
if __name__ == "__main__":
    num_samples = 2
    T = 10000
    sample_rate = 200
    speed_kmh = 5
    noise_level = 0.01

    dataset = creation_dataset(num_samples, T, sample_rate, speed_kmh, noise_level)
    for idx, (real_traj, noisy_traj) in enumerate(dataset):
        print(f"Sample {idx+1}: Real Trajectory - {len(real_traj)} points, Noisy Trajectory - {len(noisy_traj)} points")
        # Utilisation de la fonction pour afficher les deux trajectoires
        plot_dual_trajectory_3D(real_traj, noisy_traj)
