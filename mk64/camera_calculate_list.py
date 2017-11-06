import sys
import math

desired_angles = [[-25,0],[-25,60],[25,60],[25,120],[-25,120],[-25,180],[25,180],[25,240],[-25,240],[-25,300],[25,300],[25,0],[75,0],[-75,0],[-75,60],[75,60],[75,120],[-75,120],[-75,180],[75,180],[75,240],[-75,240],[-75,300],[75,300]]
                  
def print_3_1(A):
  print "(" + str(A[0]) + ", " + str(A[1]) + ", " + str(A[2]) + ")"

def print_3_3(A):
  print "" + str(A[0][0]) + ", " + str(A[0][1]) + ", " + str(A[0][2]) + ""
  print "" + str(A[1][0]) + ", " + str(A[1][1]) + ", " + str(A[1][2]) + ""
  print "" + str(A[2][0]) + ", " + str(A[2][1]) + ", " + str(A[2][2]) + ""

def mult_3_3_3_1(A, B):
  return [A[0][0] * B[0] + A[0][1] * B[1] + A[0][2] * B[2],
          A[1][0] * B[0] + A[1][1] * B[1] + A[1][2] * B[2],
          A[2][0] * B[0] + A[2][1] * B[1] + A[2][2] * B[2]]
  
def rotationMatrixX(angle):
  return [[1, 0,                0],
          [0, math.cos(angle), -math.sin(angle)],
          [0, math.sin(angle),  math.cos(angle)]]
          
def rotationMatrixY(angle):
  return [[math.cos(angle), 0, math.sin(angle)],
          [0,               1,  0],
          [-math.sin(angle), 0,  math.cos(angle)]]

def rotationMatrixZ(angle):
  return [[math.cos(angle), -math.sin(angle), 0],
          [math.sin(angle),  math.cos(angle), 0],
          [0,                0,               1]]


def calc_camera_data(camera_pos, look_pos):

  up_vector = [0, 0, 1]
  
  # Calculate look vector starting at (0,0,0)
  look_vector = [look_pos[0] - camera_pos[0], look_pos[1] - camera_pos[1], look_pos[2] - camera_pos[2]]
  # print_3_1(look_vector)
  look_mag = math.sqrt(look_vector[0] ** 2 + look_vector[1] ** 2 + look_vector[2] ** 2)

  # Calculate up vector -> look vector rejection
  # A*B
  temp1 = up_vector[0] * look_vector[0] + up_vector[1] * look_vector[1] + up_vector[2] * look_vector[2]
  # B*B
  temp2 = look_vector[0] * look_vector[0] + look_vector[1] * look_vector[1] + look_vector[2] * look_vector[2]

  temp1 = temp1 / temp2
  # *B
  temp1 = [look_vector[0] * temp1, look_vector[1] * temp1, look_vector[2] * temp1]
  #A-
  up_rejection = [up_vector[0] - temp1[0], up_vector[1] - temp1[1], up_vector[2] - temp1[2]]

  # Calculate angle between (x,y) of up rejection and XZ plane
  # Formula: (A*B)/(|A|*|B|)  =  cos(angle)
  temp3 = [up_rejection[0], up_rejection[1], 0]
  xz_plane_vec = [1,0,0]
  temp1 = xz_plane_vec[0] * temp3[0] + xz_plane_vec[1] * temp3[1] + xz_plane_vec[2] * temp3[2]
  temp2 = math.sqrt(temp3[0] ** 2 + temp3[1] ** 2 + temp3[2] ** 2)

  yaw2_angle = math.acos(temp1 / temp2)
  
  if (temp3[1] < 0):
    yaw2_angle = -yaw2_angle
    
  if (look_vector[2] > 0):
    yaw2_angle = math.pi + yaw2_angle
    
  
  
  #print math.degrees(yaw2_angle)
  
  data_results = []
  
  for angle_data in desired_angles:
  # Apply pitch angle to a X unit vector
    result_vector = [1,0,0]
    result_vector = mult_3_3_3_1(rotationMatrixY(math.radians(-angle_data[0])), result_vector)

    # Apply yaw
    result_vector = mult_3_3_3_1(rotationMatrixZ(math.radians(angle_data[1])), result_vector)
    result_vector = mult_3_3_3_1(rotationMatrixZ(yaw2_angle), result_vector)

    result_vector = [result_vector[0] * look_mag, result_vector[1] * look_mag, result_vector[2] * look_mag]
    result_vector = [camera_pos[0] + result_vector[0], camera_pos[1] + result_vector[1], camera_pos[2] + result_vector[2]]
    
    
    up_result_vector = [0,0,1]
    
    #print_3_1(result_vector)
    data_results.append("%0.10f" % result_vector[0] + ",%0.10f" % result_vector[1] + ",%0.10f" % result_vector[2] + ",%0.10f" % up_result_vector[0] + ",%0.10f" % up_result_vector[1] + ",%0.10f" % up_result_vector[2])
    
  return data_results


f = open(sys.argv[1],'r')

while True:
    x = f.readline()
    x = x.rstrip()
    if not x: break
    parts = x.split(",")
    
    data = calc_camera_data([float(parts[1]), float(parts[2]), float(parts[3])], [float(parts[4]), float(parts[5]), float(parts[6])])
    for num, line in enumerate(data, start=1):
      print "%i" % (int(parts[0])) + ",%i" % num + "," + ",".join(parts[1:4]) + "," + line + "," + ",".join(parts[10:13])
    