"""
Properties to support the molecule visualiser.
"""

# The covalent radii used to draw the radii of elements in the molecule visualiser.
covalent_radii = {
	"H": 0.31, "C": 0.76, "N": 0.71, "O": 0.66,
	"He": 0.28, "F": 0.57, "B": 0.85, "Cl": 1.02,
	"S": 1.05, "P": 1.07, "Si": 1.11, "Br": 1.20,
}

# The colors for each element when displayed in the molecule visualiser.
atom_color = {
	"H": (255,255,255),
	"C": (30,30,30),
	"N": (40,40,200),
	"O": (200,20,20),
	"S": (200,200,50),
}