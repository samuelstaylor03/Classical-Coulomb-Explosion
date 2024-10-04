import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from matplotlib.ticker import FuncFormatter
import os
import matplotlib

# Set global font to Times New Roman
mpl.rcParams['font.family'] = 'Times New Roman'
mpl.rcParams['font.weight'] = 'bold'
mpl.rcParams['axes.labelweight'] = 'bold'
mpl.rcParams['axes.labelsize'] = 24  # increase label font size
mpl.rcParams['xtick.labelsize'] = 22  # increase x tick font size
mpl.rcParams['ytick.labelsize'] = 22  # increase y tick font size
mpl.rcParams['legend.fontsize'] = 16  # Legend font size

matplotlib.rc('font', family='Times New Roman')  # set default font to Times New Roman

C_mass = 1243.7123176930008 # (eV_fs^2/A^2)
H_mass = 103.64269314108340 # (eV_fs^2/A^2)

def read_trajectory(file, num_atoms):
    with open(file, 'r') as f:
        lines = f.readlines()

    if lines[0].strip() != str(num_atoms):
        raise ValueError(f'Number of atoms in the file ({lines[0].split()[0]}) does not match the expected number '
                         f'of atoms ({num_atoms})')
    iterations = []
    positions = [[] for _ in range(num_atoms)]  # Create an empty list for each atom
    distances = []

    for i in range(0, len(lines), num_atoms + 2):  # +2 for iteration and blank line
        iterations.append(int(lines[i + 1].split('=')[1].split()[0]))
        atom_positions = []
        for j in range(num_atoms):
            atom_pos = np.array(list(map(float, lines[i + 2 + j].split()[1:])))
            positions[j].append(atom_pos)
            atom_positions.append(atom_pos)

        # Calculate the distance between first two atoms (or any other pair)
        distance = np.linalg.norm(atom_positions[0] - atom_positions[1])
        distances.append(distance)

    return iterations, positions, distances


def calculate_velocity(positions, time):
    velocities = [np.diff(atom_positions, axis=0) / np.diff(time)[:, None] for atom_positions in positions]
    speeds = [np.linalg.norm(vel, axis=1) for vel in velocities]
    return speeds


def calculate_acceleration(speeds, time):
    accelerations = [np.diff(atom_speeds) / np.diff(time[1:]) for atom_speeds in speeds]
    return accelerations


def plot_distance(time, distances, directory, mode='',show=False):
    plt.plot(time, distances,color='black')
    if mode.lower().startswith('s'):
        plt.axvline(x=25, color='#ee87ee', linestyle='--')  # Add vertical dashed line at time=25
    plt.xlabel('Time (fs)')
    plt.ylabel('Distance (Å)')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(directory, 'distance.png'))
    if show:
        plt.show()
    plt.close()


def plot_positions(time, positions, directory, labels, mode='',show=False):
    for i, pos in enumerate(positions):
        distance = np.linalg.norm(pos, axis=1)
        # Ensure Times New Roman is applied for atom names in LaTeX math mode
        plt.plot(time, distance, label=f'{labels[i]}')
    if mode.lower().startswith('s'):
        plt.axvline(x=25, color='#ee87ee', linestyle='--')  # Add vertical dashed line at time=25
    
    plt.xlabel('Time (fs)')
    plt.ylabel('Distance from origin (Å)')
    plt.grid(True)
    plt.legend(prop={'family': 'Times New Roman'})
    plt.tight_layout()
    plt.savefig(os.path.join(directory, 'position.png'))
    if show:
        plt.show()
    plt.close()


def plot_velocity(time, speeds, directory, labels, mode='',show=False):
    for i, speed in enumerate(speeds):
        # Ensure Times New Roman is applied for atom names in LaTeX math mode
        plt.plot(time[1:], speed, label=f'{labels[i]}')
    if mode.lower().startswith('s'):
        plt.axvline(x=25, color='#ee87ee', linestyle='--')  # Add vertical dashed line at time=25
    plt.xlabel('Time (fs)')
    plt.ylabel('Speed (Å/fs)')
    plt.grid(True)
    plt.legend(prop={'family': 'Times New Roman'})
    plt.tight_layout()    
    plt.savefig(os.path.join(directory, 'velocity.png'))
    if show:
        plt.show()
    plt.close()


def plot_acceleration(time, accelerations, directory, labels, mode='',show=False):
    for i, accel in enumerate(accelerations):
        # Ensure Times New Roman is applied for atom names in LaTeX math mode
        plt.plot(time[2:], accel, label=f'{labels[i]}')
    
    if mode.lower().startswith('s'):
        plt.axvline(x=25, color='#ee87ee', linestyle='--')  # Add vertical dashed line at time=25
    plt.xlabel('Time (fs)')
    plt.ylabel('Acceleration (Å/fs²)')
    plt.grid(True)
    plt.legend(prop={'family': 'Times New Roman'})
    plt.tight_layout()
    plt.savefig(os.path.join(directory, 'acceleration.png'))
    if show:
        plt.show()
    plt.close()


def plot_force(time, accelerations, masses, directory, labels, mode='',show=False):
    for i, accel in enumerate(accelerations):
        force = masses[i] * accel
        # Ensure Times New Roman is applied for atom names in LaTeX math mode
        plt.plot(time[2:], force, label=f'{labels[i]}')
    if mode.lower().startswith('s'):
        plt.axvline(x=25, color='#ee87ee', linestyle='--')  # Add vertical dashed line at time=25
    plt.xlabel('Time (fs)')
    plt.ylabel('Force (eV²/Å)')
    plt.grid(True)
    plt.legend(prop={'family': 'Times New Roman'})
    plt.tight_layout()
    plt.savefig(os.path.join(directory, 'force.png'))
    if show:
        plt.show()
    plt.close()


# Example usage
trajectory_file_list=['','','']
'''
trajectory_file_list[0] = 'data\\c2h2_classical\\trajectory_r1.xyz'
trajectory_file_list[1] = 'data\\c2h2_semi_classical\\trajectory_r1.xyz'
trajectory_file_list[2] = 'data\\c2h2_quantum\\trajectory_r1.xyz'
'''

trajectory_file_list[0] = 'data\\c4h10_classical\\14\\trajectory_r1.xyz'
trajectory_file_list[1] = 'data\\c4h10_semi_classical\\14\\trajectory_r1.xyz'
trajectory_file_list[2] = 'data\\c4h10_quantum\\14\\trajectory_r1.xyz'

modes=['','s','']

num_carbon_atoms = 4
num_hydrogen_atoms = 10
total_atoms = num_carbon_atoms + num_hydrogen_atoms

show=False


for i in range(0,len(trajectory_file_list)): 
    trajectory_file=trajectory_file_list[i]
    mode=modes[i]
    labels = ['C'] * num_carbon_atoms + ['H'] * num_hydrogen_atoms
    masses = [C_mass] * num_carbon_atoms + [H_mass] * num_hydrogen_atoms

    iterations, positions, distances = read_trajectory(trajectory_file, total_atoms)
    directory = os.path.dirname(trajectory_file)
    time = np.array(iterations) / 1000  # convert iterations to time in fs
    speeds = calculate_velocity(positions, time)
    accelerations = calculate_acceleration(speeds, time)

    plot_distance(time, distances, directory,mode=mode,show=show)
    plot_positions(time, positions, directory, labels,mode=mode,show=show)
    plot_velocity(time, speeds, directory, labels,mode=mode,show=show)
    plot_acceleration(time, accelerations, directory, labels,mode=mode,show=show)
    plot_force(time, accelerations, masses, directory, labels,mode=mode,show=show)

print("Finished. All graphs generated.")