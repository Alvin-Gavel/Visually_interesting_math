import numpy as np
import matplotlib.pyplot as plt

def make_xy(n, radius = 1, start_angle = 0):
   angles = start_angle + (2 * np.pi / n) * np.arange(0, n)
   return np.cos(angles) * radius, np.sin(angles) * radius  

def figure_dimensions():
   x_min, x_max = plt.xlim()
   y_min, y_max = plt.ylim()
   r = max(abs(x_min), abs(y_min), x_max, y_max)
   x_left, x_right, y_low, y_high = -r, r, -r, r
   plt.xlim(x_left, x_right)
   plt.ylim(y_low, y_high)
   plt.axis('off')
   fig = plt.gcf()
   fig.set_size_inches(5, 5)
   return

def draw_star_polygon(n, k, plot_folder_path, filename_kernel = '', mode = "default", repetitions = 1, repetition_contact = "middle", labels = [], label_mode = ''):
   def draw(start_angle, radius):
      x, y = make_xy(n, radius = radius, start_angle = start_angle)
      
      for i in range(n):
         if mode == "shaded":
            d = np.gcd(n, k)
            c = np.linspace(0, 0.8, num = d)
            c_string = '{}'.format(c[i%d])
         elif mode == "inscribed":
            c_string = "gray"
         else:
            c_string = 'k'
         plt.plot([x[i], x[i-k]], [y[i], y[i-k]], ls="-", c=c_string)
      return
         
   def draw_until_intersect(start_angle, radius):
      if mode == "inwards":
         c = np.linspace(0, 0.8, num = k)
      elif mode == "outwards":
         c = np.linspace(0.8, 0, num = k)
      elif mode == "alternating":
         c = ([0.6, 0] * int(np.ceil(k / 2)))[0:k]
      intersect_radius = radius
      rotate = 0
      for k_red in reversed(range(2, k+1)):
         c_string = '{}'.format(c[(k_red-1)%(k)])
         x, y = make_xy(n, radius = intersect_radius, start_angle = start_angle + rotate * np.pi / n)
         intersect_radius *= np.sin((1/2 - k_red/n) * np.pi) / np.sin((1/2 + (k_red-1)/n) * np.pi)
         rotate += 1
         x_int, y_int = make_xy(n, radius = intersect_radius, start_angle = start_angle + rotate * np.pi / n)
         for i in range(n):
            plt.plot([x[i], x_int[i]], [y[i], y_int[i]], ls="-", c=c_string)
            plt.plot([x[i], x_int[i-1]], [y[i], y_int[i-1]], ls="-", c=c_string)
            
      c_string = '{}'.format(c[0])
      for i in range(n):
         plt.plot([x_int[i], x_int[i-1]], [y_int[i], y_int[i-1]], ls="-", c=c_string)
      return
   
   def add_labels(start_angle, radius):
      n_labels = len(labels)
      angle_increment = 2 * np.pi / n
      for i in range(n):
         theta = angle_increment * i
         if i % (n // n_labels) == 0:
            if label_mode == 'radial':
               rotation = np.degrees(theta)
               horizontalalignment = 'left'
            elif label_mode == 'horisontal':
               rotation = 0
               if 3 * np.pi / 2 > theta > np.pi / 2:
                  horizontalalignment = 'right'
               elif theta == 3 * np.pi / 2 or theta == np.pi / 2:
                  horizontalalignment = 'center'
               else:
                  horizontalalignment = 'left'
            plt.annotate(labels[i // (n // n_labels)], (theta, 1.1), xycoords = 'polar', rotation = rotation, rotation_mode = 'anchor', verticalalignment = 'center', horizontalalignment = horizontalalignment)
   
   if mode not in ["default", "shaded", "inscribed", "inwards", "outwards", "alternating"]:
      print("Cannot recognise mode")
      return
   if repetition_contact not in ["middle", "intersection"]:
      print("Cannot recognise repetition contact")
      return
   if len(labels) != 0:
      if n % len(labels) != 0:
         print("Number of nodes must be evenly divisible by length of label vector!")
         return
      if label_mode not in ['radial', 'horisontal']:
         print("Cannot recognise label mode")
         return
      
   alpha = (1 - 2*k/n) * np.pi
   inscribed_circle_radius = np.sin(alpha / 2)

   offset_angle = 0
   radius = 1
   for i in range(repetitions):
      if mode in ["inwards", "outwards", "alternating"]:
         draw_until_intersect(offset_angle, radius)
      else:
         draw(offset_angle, radius)
      if repetition_contact == "middle":
         offset_angle += (np.pi / n) * (k % 2)
         radius *= inscribed_circle_radius
      elif repetition_contact == "intersection":
         offset_angle += (np.pi / n) * ((k+1) % 2)
         radius *= np.sin(np.pi * (1/2 - k/n)) / np.sin(np.pi * (1/2 - 1/n))

   if mode == "inscribed":
      circle_x, circle_y = make_xy(10000, radius = inscribed_circle_radius, start_angle = 0)
      plt.plot(circle_x, circle_y, ls="--", c='k')
   
   if len(labels) != 0:
      add_labels(0, 1)
      
   figure_dimensions()
   
   if filename_kernel != '':
      filename = filename_kernel + '_'
   else:
      filename = filename_kernel
   
   filename += "{}_{}".format(n, k)
   if not mode == "default":
      filename += "_{}".format(mode)
   if repetitions > 1:
      filename += "_repeat_{}_contact_{}".format(repetitions, repetition_contact)
   filename += ".png"
   plt.savefig("{}/{}".format(plot_folder_path, filename), format = 'png', bbox_inches = 'tight')
   plt.close()
   return

def draw_star_polygons_with_fixed_n(n, plot_folder_path, filename_kernel = '', mode = "default", repetitions = 1, repetition_contact = "middle", labels = [], label_mode = ''):
   for k in range(1, n // 2 + 1):
      for rep in range(1, repetitions+1):
         if not ((rep > 1 and k == 1 and repetition_contact == "intersection") or k == 1 and mode in ["inwards", "outwards", "alternating"]):
            draw_star_polygon(n, k, plot_folder_path, filename_kernel = filename_kernel, mode = mode, repetitions = rep, repetition_contact = repetition_contact, labels = labels, label_mode = label_mode)
   return

def draw_star_polygons_below(n_max, plot_folder_path, mode = "default", repetitions = 1, repetition_contact = "middle"):
   for n in range(3, n_max):
      draw_star_polygons_with_fixed_n(n, plot_folder_path, mode = mode, repetitions = repetitions, repetition_contact = repetition_contact)
   return
