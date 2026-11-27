import matplotlib.pyplot as plt

#%% ==== Functions ====

def apply_plot_settings(size='normal'):
    """Apply default plot settings."""
    plt.rcParams.update({
        # Figure and save settings
        'figure.dpi': 100,
        'savefig.dpi': 300,
        'font.family': 'sans-serif',
        'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
        'pdf.fonttype': 42,
        'figure.facecolor': 'none',   # Background of the entire figure
        'axes.facecolor': 'none',     # Background of the axes
        'savefig.facecolor': 'none',  # Background when saving
        'savefig.transparent': True,  # Save as transparent
        # Size settings
        # 'figure.figsize': (8, 6),
    })
    update_plot_settings(size=size)


def update_background_color(color='white'):
    """Change the background color of the figure and axes."""
    plt.rcParams.update({
        'figure.facecolor': color,   # Background of the entire figure
        'axes.facecolor': color,     # Background of the axes
        'savefig.facecolor': color,  # Background when saving
        'savefig.transparent': False,  # Save as non-transparent
    })


def update_plot_settings(size='normal'):
    """Update plot settings for specific use cases."""
    if size == 'normal':
        plt.rcParams.update({
            'font.size': 10,
            'axes.titlesize': 12,
            'axes.labelsize': 10,
            'xtick.labelsize': 10,
            'ytick.labelsize': 10,
            'legend.fontsize': 10,
        })
    elif size == 'small':
        plt.rcParams.update({
            'font.size': 8,
            'axes.titlesize': 10,
            'axes.labelsize': 8,
            'xtick.labelsize': 8,
            'ytick.labelsize': 8,
            'legend.fontsize': 8,
        })

    elif size == 'large':
        plt.rcParams.update({
            'font.size': 14,
            'axes.titlesize': 16,
            'axes.labelsize': 14,
            'xtick.labelsize': 14,
            'ytick.labelsize': 14,
            'legend.fontsize': 14,
        })

    elif size == 'x-large':
        plt.rcParams.update({
            'font.size': 16,
            'axes.titlesize': 18,
            'axes.labelsize': 16,
            'xtick.labelsize': 16,
            'ytick.labelsize': 16,
            'legend.fontsize': 16,
        })

    elif size == 'xx-large':
        plt.rcParams.update({
            'font.size': 18,
            'axes.titlesize': 20,
            'axes.labelsize': 18,
            'xtick.labelsize': 18,
            'ytick.labelsize': 18,
            'legend.fontsize': 18,
        })

    elif size == 'xxx-large':
        plt.rcParams.update({
            'font.size': 20,
            'axes.titlesize': 22,
            'axes.labelsize': 20,
            'xtick.labelsize': 20,
            'ytick.labelsize': 20,
            'legend.fontsize': 20,
        })
    else:
        print(f"Unknown plot size: {size}. No changes made to plot settings.")
        pass


from matplotlib.colors import LinearSegmentedColormap
# Define custom color map
custom_cmap = LinearSegmentedColormap.from_list("my_cmap", [
    "#00ac00",
    "#2fb500",
    "#b7db00",
    "#e7ce1e",
    "#ebb166",
    "#f0f0f0",
][::-1], N=256)  # Reverse the list order.


#%% ==== Apply default plot settings ====
apply_plot_settings(size='xxx-large')

