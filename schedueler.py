import random
def shortest_time_remaining(processes=[]):
  arrival_times = sorted(set(map(lambda (a,b,c,d): c, processes)))
  currently_running = None
  quantums = 0
  while True:
    if (len(arrival_times) and quantums == arrival_times[0]):
      arrival_times = arrival_times[1:]
      if currently_running:
        processes.append(currently_running)
      currently_running = None

    if not currently_running:
      available_processes = [(a,b,c,d) for (a,b,c,d) in processes if c <=
        quantums]
      if available_processes:
        currently_running = min(available_processes, key = lambda (a,b,c,d): d)
        processes.remove(currently_running)
      else:
        print "No processes running at time", quantums
        quantums += 1
        continue

    name, user, starttime, remaining = currently_running
    remaining -= 1

    print "At time %i" % int(quantums),
    print name, "remaining time:", remaining

    if remaining:
      currently_running = (name, user, starttime, remaining)
    else:
      currently_running = None
      print "process %s has finished" % name

    quantums +=1

    if currently_running == None and len(processes) == 0:
      break

def lottery(processes=[], priorities=[]):
  box = []
  for (name, owner, starttime, remaining) in processes:
    username, priority = filter(lambda (a,b): a==owner, priorities)[0]
    box += [(name, starttime)]*priority
  quantums = 0
  while True:
    available = filter(lambda (a,b): b <= quantums, box)
    if available:
      index = random.randrange(len(available))
      name, starttime = available[index]
      name, user, starttime, remaining =\
        filter(lambda (a,b,c,d): a == name, processes)[0]
      remaining -= 2
      if rem
      remaining = remaining >= 0 and remaining or 0
      processes = filter(lambda (a,b,c,d): a != name, processes)
      if remaining > 0:
        processes.append((name, user, starttime, remaining))
        next_quantum = quantums + 2
      else:
        box = filter(lambda (a,b): a != name, box)
        next_quantum = quantums + 1
      print "Frome time %i to %i: %s remaining time: %i" % (quantums,
      next_quantum, name, remaining)
      quantums = next_quantum
      if remaining <= 0:
        print "Process %s has finished" % name
      if not processes:
        break
    else:
      print "No processes are running at time %i" % quantums
      quantums += 1


print "Start of STR"
shortest_time_remaining([("A","Mohamed",1,3), ("B","Mohamed",2,1),
("C","Mohamed",3,1), ("D","Mohamed",8,3)])

print "\n\nStart of lottery"
processes = [("A","Mohamed",1,10), ("B","Nourhan",2,7), ("C","Mohamed",3,5), ("D","Nourhan",8,3)]
priorities = [("Mohamed", 1), ("Nourhan", 9)]
print processes
print priorities
lottery(processes, priorities)
