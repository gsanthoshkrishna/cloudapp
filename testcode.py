def a():
    #select  res_prop_id from resource_prop where prop_name = 'name' and  res_id = 3
    p_name = 'name'
    r_id ='3'
    query = "select  res_prop_id from resource_prop where prop_name = '" + p_name + "' and  res_id = " + r_id 
    print(query)

    #num = "1"
    #these are 2s factors
    #these are 5s factors
    #these are 11s factors
    #temp = "these are " + num + "s"
   # print(temp)
    


#a()

# Correct dictionary definition
#my_dict = {'key1': 'value1', 'key2': 'value2'}

# Print the dictionary
#print(my_dict)

# Iterate over the dictionary and print each key
#for x in my_dict:
    #print(x)

def test():
    unique_id = '12345'
    prefix = 'sqrl'
    print("test")
    res_unique_id =  prefix +"-" + unique_id  
    print(res_unique_id)
test()

    
  
