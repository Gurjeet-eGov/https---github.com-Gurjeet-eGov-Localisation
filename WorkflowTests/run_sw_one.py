from SW import NewSW

if __name__ == '__main__':
    try:
        conn = NewSW()
        print('NewSW completed, Connection ID:', conn)
    except Exception as e:
        import traceback
        print('NewSW failed:')
        traceback.print_exc()
